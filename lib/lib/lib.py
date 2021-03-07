# -*- coding: utf-8 -*-
import json
import logging
import urllib.request

logger = logging.getLogger()

class Lib:
    def __init__(self, endpoint_url, credential):
        self._endpoint_url = endpoint_url
        self._credentail = credential

    def create_organization(self, data):
        url = "https://%s/organization" % self._endpoint_url
        body = json.dumps(data).encode()
        req = urllib.request.Request(url=url, data=body, headers={}, method='POST')

        organization_id = None
        try:
            with urllib.request.urlopen(req) as res:
                body = json.load(res)
                organization_id = body['organization_id']
        except urllib.error.HTTPError as err:
            logger.error(f'{err}')
            raise ValueError("create_organization: Failed to request.")
        except urllib.error.URLError as err:
            logger.error(f'{err}')
            raise ValueError("create_organization: Failed to request.")

        logger.info("create_organization: Successfully create organization.")
        return organization_id

    def create_user(self, organization_id, data):
        params = {
            'organization_id': organization_id,
        }
        url = "https://%s/user?=%s" % (self._endpoint_url, urllib.parse.urlencode(params))
        body = json.dumps(data).encode()
        req = urllib.request.Request(url=url, data=body, headers={}, method='POST')

        user_id = None
        try:
            with urllib.request.urlopen(req) as res:
                body = json.load(res)
                user_id = body['user_id']
        except urllib.error.HTTPError as err:
            logger.error(f'{err}')
            raise ValueError("create_user: Failed to request.")
        except urllib.error.URLError as err:
            logger.error(f'{err}')
            raise ValueError("create_user: Failed to request.")

        logger.info("create_user: Successfully create user.")
        return user_id

    def set_password(self, organization_id, user_id, password):
        params = {
            'organization_id': organization_id,
        }
        url = "https://%s/user/%s?=%s" % (
            self._endpoint_url, user_id, urllib.parse.urlencode(params))

        data = json.dumps({'password': password}).encode()
        req = urllib.request.Request(url=url, data=data, headers={}, method='POST')

        result = None
        try:
            with urllib.request.urlopen(req) as res:
                body = json.load(res)
                result = body['result']
        except urllib.error.HTTPError as err:
            logger.error(f'{err}')
            raise ValueError("set_password: Failed to request.")
        except urllib.error.URLError as err:
            logger.error(f'{err}')
            raise ValueError("set_password: Failed to request.")

        logger.info("set_password: Successfully set password.")
        return result

    def sign_in(self, username, password):
        url = "https://%s/signIn" % self._endpoint_url
        req = urllib.request.Request(url=url, headers={}, method='POST')

        result = None
        try:
            with urllib.request.urlopen(req) as res:
                body = json.load(res)
                result = body['result']
        except urllib.error.HTTPError as err:
            logger.error(f'{err}')
            raise ValueError("sign_in: Failed to request.")
        except urllib.error.URLError as err:
            logger.error(f'{err}')
            raise ValueError("sign_in: Failed to request.")

        logger.info("sign_in: Successfully sign in.")
        return result