# -*- coding: utf-8 -*-
import pytest
import re
import json
import uuid

import boto3
from moto import mock_secretsmanager

from app import app

credentials = {}

class MockResponse():
    def __init__(self, body, code = 200):
        self._body = body
        self.code = code

    def __enter__(self):
        return self

    def read(self):
        return json.dumps(self._body)

    def __exit__(self, exc_type, exc_value, tb):
        pass

credentials = {
    'credential': 'test'
}

@mock_secretsmanager
def test_create_secret_initial(mocker):
    secret_id = 'test-secret'
    client = boto3.client('secretsmanager', region_name='us-east-1')
    client.create_secret(Name=secret_id, SecretString="{}")
    token = str(uuid.uuid4())
    secrets = {}

    client.put_secret_value(
        SecretId=secret_id,
        ClientRequestToken=token,
        SecretString=json.dumps(secrets),
        VersionStages=['AWSPENDING']
    )

    # moto does not mock get_secret_value with VersionId or VersionStage
    responses = [
        {},
        { 'SecretString': json.dumps(credentials) },
        client.exceptions.ResourceNotFoundException({}, 'get_secret_value')
    ]
    mocker.patch.object(client, "get_secret_value", side_effect=responses)
    response = MockResponse({
        'organization_id': 'organization_id',
        'user_id': 'user_id',
        'result': 'success'
    })
    mocker.patch("urllib.request.urlopen", return_value=response)

    app.create_secret(client, secret_id, token)

@mock_secretsmanager
def test_create_secret_rotation(mocker):
    secret_id = 'test-secret'
    client = boto3.client('secretsmanager', region_name='us-east-1')
    client.create_secret(Name=secret_id, SecretString="{}")
    token = str(uuid.uuid4())
    secrets = {
        'organization_id': 'organization_id',
        'user_id': 'user_id',
        'username': 'username',
        'password': 'password'
    }

    client.put_secret_value(
        SecretId=secret_id,
        ClientRequestToken=token,
        SecretString=json.dumps(secrets),
        VersionStages=['AWSPENDING']
    )

    # moto does not mock get_secret_value with VersionId or VersionStage
    responses = [
        { 'SecretString': json.dumps(secrets) },
        client.exceptions.ResourceNotFoundException({}, 'get_secret_value')
    ]
    mocker.patch.object(client, "get_secret_value", side_effect=responses)

    response = MockResponse({
        'organization_id': 'organization_id',
        'user_id': 'user_id',
        'result': 'success'
    })
    mocker.patch("urllib.request.urlopen", return_value=response)

    app.create_secret(client, secret_id, token)

@mock_secretsmanager
def test_create_secret_pendings(mocker):
    secret_id = 'test-secret'
    client = boto3.client('secretsmanager', region_name='us-east-1')
    client.create_secret(Name=secret_id, SecretString="{}")
    token = str(uuid.uuid4())
    secrets = {
        'organization_id': 'organization_id',
        'user_id': 'user_id',
        'username': 'username',
        'password': 'password'
    }

    client.put_secret_value(
        SecretId=secret_id,
        ClientRequestToken=token,
        SecretString=json.dumps(secrets),
        VersionStages=['AWSPENDING']
    )

    # moto does not mock get_secret_value with VersionId or VersionStage
    response = { 'SecretString': json.dumps(secrets) }
    mocker.patch.object(client, "get_secret_value", return_value=response)

    response = MockResponse({ 'result': 'success' })
    mocker.patch("urllib.request.urlopen", return_value=response)

    app.create_secret(client, secret_id, token)

@mock_secretsmanager
def test_set_secret(mocker):
    secret_id = 'test-secret'
    client = boto3.client('secretsmanager', region_name='us-east-1')
    client.create_secret(Name=secret_id, SecretString="{}")
    token = str(uuid.uuid4())
    secrets = {
        'organization_id': 'organization_id',
        'user_id': 'user_id',
        'username': 'username',
        'password': 'password'
    }

    client.put_secret_value(
        SecretId=secret_id,
        ClientRequestToken=token,
        SecretString=json.dumps(secrets),
        VersionStages=['AWSPENDING']
    )

    # moto does not mock get_secret_value with VersionId or VersionStage
    response = { 'SecretString': json.dumps(secrets) }
    mocker.patch.object(client, "get_secret_value", return_value=response)

    response = MockResponse({ 'result': 'success' })
    mocker.patch("urllib.request.urlopen", return_value=response)

    app.set_secret(client, secret_id, token)

@mock_secretsmanager
def test_test_secret(mocker):
    secret_id = 'test-secret'
    client = boto3.client('secretsmanager', region_name='us-east-1')
    client.create_secret(Name=secret_id, SecretString="{}")
    token = str(uuid.uuid4())
    secrets = {
        'organization_id': 'organization_id',
        'user_id': 'user_id',
        'username': 'username',
        'password': 'password'
    }

    client.put_secret_value(
        SecretId=secret_id,
        ClientRequestToken=token,
        SecretString=json.dumps(secrets),
        VersionStages=['AWSPENDING']
    )

    # moto does not mock get_secret_value with VersionId or VersionStage
    response = { 'SecretString': json.dumps(secrets) }
    mocker.patch.object(client, "get_secret_value", return_value=response)

    response = MockResponse({ 'result': 'success' })
    mocker.patch("urllib.request.urlopen", return_value=response)

    app.test_secret(client, secret_id, token)

@mock_secretsmanager
def test_finish_secret(mocker):
    secret_id = 'test-secret'
    client = boto3.client('secretsmanager')
    client.create_secret(Name=secret_id, SecretString="{}")
    token = str(uuid.uuid4())

    # moto does not mock update_secret_version_stage
    mocker.patch.object(client, "update_secret_version_stage", return_value=None)

    app.finish_secret(client, secret_id, token)

def test_create_organization(mocker):
    response = MockResponse({ 'organization_id': 'organization_id' })
    mocker.patch("urllib.request.urlopen", return_value=response)

    organization_id = app.create_organization(credentials)
    assert organization_id == 'organization_id'

def test_create_user(mocker):
    response = MockResponse({ 'user_id': 'user_id' })
    mocker.patch("urllib.request.urlopen", return_value=response)

    organization_id = 'organization_id'
    username = app.create_username(8)
    user_id = app.create_user(organization_id, username, credentials)
    assert user_id == 'user_id'

def test_set_password(mocker):
    response = MockResponse({ 'result': 'success' })
    mocker.patch("urllib.request.urlopen", return_value=response)

    secrets = {
        'organization_id': 'organization_id',
        'user_id': 'user_id',
        'username': 'username',
        'password': 'password'
    }
    result = app.set_password(secrets, credentials)
    assert result == 'success'

def test_sign_in(mocker):
    response = MockResponse({ 'result': 'success' })
    mocker.patch("urllib.request.urlopen", return_value=response)

    secrets = {
        'organization_id': 'organization_id',
        'user_id': 'user_id',
        'username': 'username',
        'password': 'password'
    }
    result = app.sign_in(secrets, credentials)
    assert result == 'success'

def test_create_username():
    username = app.create_username(8)
    assert re.match(r'^sys-[a-z0-9]{8}@example\.com$', username)