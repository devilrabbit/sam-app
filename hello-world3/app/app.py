# -*- coding: utf-8 -*-
import boto3
import json
import logging
import os
import random
import string
from lib.lib import Lib

ENDPOINT = os.environ.get('ENDPOINT', '')
CREDENTIAL_SECRET_ID = os.environ.get('CREDENTIAL_SECRET_ID', 'credentials')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    secret_id = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    endpoint_url = os.environ.get('SECRETS_MANAGER_ENDPOINT', 'https://secretsmanager.amazonaws.com')
    client = boto3.client('secretsmanager', endpoint_url=endpoint_url)

    metadata = client.describe_secret(SecretId=secret_id)
    if not metadata['RotationEnabled']:
        logger.error("Secret %s is not enabled for rotation" % secret_id)
        raise ValueError("Secret %s is not enabled for rotation" % secret_id)

    versions = metadata['VersionIdsToStages']
    if token not in versions:
        logger.error("Secret version %s has no stage for rotation of secret %s." % (token, secret_id))
        raise ValueError("Secret version %s has no stage for rotation of secret %s." % (token, secret_id))

    if "AWSCURRENT" in versions[token]:
        logger.info("Secret version %s already set as AWSCURRENT for secret %s." % (token, secret_id))
        return
    elif "AWSPENDING" not in versions[token]:
        logger.error("Secret version %s not set as AWSPENDING for rotation of secret %s." % (token, secret_id))
        raise ValueError("Secret version %s not set as AWSPENDING for rotation of secret %s." % (token, secret_id))

    if step == "createSecret":
        create_secret(client, secret_id, token)
    elif step == "setSecret":
        set_secret(client, secret_id, token)
    elif step == "testSecret":
        test_secret(client, secret_id, token)
    elif step == "finishSecret":
        finish_secret(client, secret_id, token)
    else:
        raise ValueError("Invalid step parameter")


def create_secret(client, secret_id, token):
    current_secrets = {}

    try:
        current_secrets = get_secrets(client, secret_id, 'AWSCURRENT')
    except KeyError:
        credential = get_credentials(client, CREDENTIAL_SECRET_ID)
        username = create_username(16)
        organization_id = create_organization(credential)
        user_id = create_user(organization_id, username, credential)
        current_secrets['organization_id'] = organization_id
        current_secrets['user_id'] = user_id
        current_secrets['username'] = username

    try:
        client.get_secret_value(SecretId=secret_id, VersionId=token, VersionStage='AWSPENDING')
        logger.info("create_secret: Successfully retrieved secret for %s." % secret_id)
    except client.exceptions.ResourceNotFoundException:
        exclude_characters = os.environ['EXCLUDE_CHARACTERS'] if 'EXCLUDE_CHARACTERS' in os.environ else '/@"\'\\'
        password = client.get_random_password(ExcludeCharacters=exclude_characters)
        current_secrets['password'] = password['RandomPassword']

        client.put_secret_value(SecretId=secret_id, ClientRequestToken=token, SecretString=json.dumps(current_secrets), VersionStages=['AWSPENDING'])
        logger.info("create_secret: Successfully put secret for secret %s and version %s." % (secret_id, token))

def set_secret(client, secret_id, token):
    try:
        pending_secrets = get_secrets(client, secret_id, 'AWSPENDING', token)
        credential = get_credentials(client, CREDENTIAL_SECRET_ID)
        set_password(pending_secrets, credential)
    except Exception:
        raise ValueError("set_secret: Failed to set secret.")

    logger.info("set_secret: Successfully set password with secret %s and version %s." % (secret_id, token))

def test_secret(client, secret_id, token):
    try:
        pending_secrets = get_secrets(client, secret_id, 'AWSPENDING', token)
        credential = get_credentials(client, CREDENTIAL_SECRET_ID)
        sign_in(pending_secrets, credential)
    except Exception:
        raise ValueError("test_secret: Failed to test secret.")

    logger.info("test_secret: Successfully signed into system with AWSPENDING secret in %s." % secret_id)

def finish_secret(client, secret_id, token):
    metadata = client.describe_secret(SecretId=secret_id)
    current_version = None
    for version in metadata['VersionIdsToStages']:
        if 'AWSCURRENT' in metadata['VersionIdsToStages'][version]:
            if version == token:
                logger.info("finish_secret: Version %s already marked as AWSCURRENT for %s" % (version, secret_id))
                return
            current_version = version
            break

    client.update_secret_version_stage(SecretId=secret_id, VersionStage='AWSCURRENT', MoveToVersionId=token, RemoveFromVersionId=current_version)
    logger.info("finish_secret: Successfully set AWSCURRENT stage to version %s for secret %s." % (token, secret_id))

def get_secrets(client, secret_id, stage, token=None):
    required_fields = ['organization_id', 'user_id', 'username', 'password']

    if token:
        secret = client.get_secret_value(SecretId=secret_id, VersionId=token, VersionStage=stage)
    else:
        secret = client.get_secret_value(SecretId=secret_id, VersionStage=stage)

    if 'SecretString' not in secret:
        raise KeyError("SecretString not set.")

    plaintext = secret['SecretString']
    secrets = json.loads(plaintext)

    for field in required_fields:
        if field not in secrets:
            err_msg = "%s key is missing from secret JSON" % field
            logger.info(err_msg)
            raise KeyError(err_msg)

    return secrets

def get_credentials(client, secret_id):
    try:
        secret = client.get_secret_value(SecretId=secret_id)
        plaintext = secret['SecretString']
        secrets = json.loads(plaintext)
        return secrets
    except:
        err_msg = "could not get credentials"
        logger.error(err_msg)
        raise KeyError(err_msg)

def create_organization(credential):
    try:
        lib = Lib(ENDPOINT, credential)
        organization_id = lib.create_organization({'name':'test'})
        logger.info("create_organization: Successfully create organization.")
        return organization_id
    except Exception:
        raise ValueError("create_organization: Failed to request.")

def create_user(organization_id, username, credential):
    try:
        lib = Lib(ENDPOINT, credential)
        user_id = lib.create_user(organization_id, {
            'email': username
        })
        logger.info("create_user: Successfully create user.")
        return user_id
    except Exception:
        raise ValueError("create_user: Failed to request.")

def set_password(secrets, credential):
    if 'organization_id' not in secrets:
        raise KeyError("organization_id is not generated")
    if 'user_id' not in secrets:
        raise KeyError("user_id is not generated")
    if 'password' not in secrets:
        raise KeyError("password is not generated")

    try:
        lib = Lib(ENDPOINT, credential)
        result = lib.set_password(
            secrets['organization_id'],
            secrets['user_id'],
            secrets['password'])
        logger.info("set_password: Successfully set password.")
        return result
    except Exception:
        raise ValueError("set_password: Failed to request.")

def sign_in(secrets, credential):
    if 'username' not in secrets:
        raise KeyError("username is not generated")
    if 'password' not in secrets:
        raise KeyError("password is not generated")

    try:
        lib = Lib(ENDPOINT, credential)
        result = lib.sign_in(
            secrets['username'],
            secrets['password'])
        logger.info("sign_in: Successfully sign in.")
        return result
    except Exception:
        raise ValueError("sign_in: Failed to request.")

def create_username(prefix_length):
    characters = [random.choice(string.ascii_lowercase + string.digits) for i in range(prefix_length)]
    return 'sys-%s@example.com' % ''.join(characters)