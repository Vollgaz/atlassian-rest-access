# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
# Author:      VollGaz
# -------------------------------------------------------------------------------

import json

from client.abstractclient import AbstractClient


class ConfluenceClient(AbstractClient):
    """Confluence server authentication object.
    Based on : https://docs.atlassian.com/atlassian-confluence/REST/latest-server/

    The user account used must have administrators rights.

    The ``ssl_verify`` parameter controls how and if certificates are verified.
    If ``True``, the SSL certificate will be verified.
    A CA_BUNDLE path can also be provided.
    """

    def __init__(self, confluence_url, user_name, user_pass, ssl_verify=True, timeout=None):
        super(self.__class__, self).__init__(confluence_url, user_name, user_pass, ssl_verify=ssl_verify, timeout=timeout)
        self.rest_url = self._url.rstrip("/") + "/rest/api"
        self.rpc_url = self._url.rstrip("/") + "/rpc/json-rpc/confluenceservice-v2"

    def get_audits(self):
        """

        :return:
        """
        self._set_json_mode()
        response = self._get(self.rest_url + "/audit",
                             params={'limit': 1000})
        if not response.ok:
            return None
        return json.loads(response.content.decode('utf-8'))['results']

    def get_groups(self):
        """

        :return:
        """
        self._set_json_mode()
        response = self._get(self.rest_url + "/group",
                             params={'limit': 1000})
        if not response.ok:
            return None
        return json.loads(response.content.decode('utf-8'))['results']

    def get_group_members(self, groupname):
        """

        :param groupname:
        :return:
        """
        self._set_json_mode()
        response = self._get(self.rest_url + "/group/" + groupname + "/member",
                             params={'limit': 1000})
        if not response.ok:
            return None
        return json.loads(response.content.decode('utf-8'))['results']

    def get_spaces(self, spacetype=""):
        """Get the list of all the available spaces (global and personal).

        Returns:
            str:
                The json string representation of the membership list.
        """
        self._set_json_mode()
        response = self._get(self.rest_url + "/space",
                             params={
                                 'type': spacetype,
                                 'limit': 1000})
        if not response.ok:
            return None
        return json.loads(response.content.decode('utf-8'))['results']

    def get_space_properties(self, spacekey):
        """

        :param spacekey:
        :return:
        """
        self._set_json_mode()
        response = self._get(self.rest_url + "/space/" + spacekey,
                             params={
                                 'expand': 'space'})
        if not response.ok:
            return None
        return json.loads(response.content.decode('utf-8'))['results']

    def get_space_permissions(self, spacekey):
        """

        :param spacekey:
        :return:
        """
        self._set_json_mode()
        data = {
            "jsonrpc": "2.0",
            "method": "getSpacePermissionSets",
            "params": [spacekey],
            "id": 12345
        }
        response = self._post(self.rpc_url,
                              data=json.dumps(data))
        if not response.ok:
            return None
        return json.loads(response.content.decode('utf-8'))['result']

    def get_user(self, username):
        """

        :param username:
        :return:
        """
        self._set_json_mode()
        data = {
            "jsonrpc": "2.0",
            "method": "getUser",
            "params": [username],
            "id": 12345
        }
        response = self._post(self.rpc_url,
                              data=json.dumps(data))
        if not response.ok:
            return None
        return json.loads(response.content.decode('utf-8'))['result']

    def get_page(self, pagename="", spacekey="", expand=""):
        """

        :param pagename:
        :param spacekey:
        :param expand:
        :return:
        """
        self._set_json_mode()
        response = self._get(self.rest_url + "/content",
                              params={
                                  'title': pagename,
                                  'spacekey': spacekey,
                                  'expand': expand
                              })
        if not response.ok:
            return None
        return json.loads(response.content.decode('utf-8'))['results']

    def update_page(self, pageid="", pageversion="", pagebody=""):
        data = {
            "version": {
                "number": pageversion
            },
            "type": "page",
            "body": {
                "storage": {
                    "value": pagebody,
                    "representation": "storage"
                }
            }
        }
        response = self._put(self.rest_url + "/content/" + pageid,
                             data=json.dumps(data))
        if not response.ok:
            return None
        return json.loads(response.content.decode('utf-8'))

    def create_new_page(self, spacekey="", ancestors=None, pagetitle="", pagebody=""):
        """

        :param ancestors:
        :param spacekey:
        :param pagetitle:
        :param pagebody:
        :return:
        """
        self._set_json_mode()
        data = {
            "type": "page",
            "ancestors" : ancestors,
            "title": pagetitle,
            "space": {
                "key": spacekey
            },
            "body": {
                "storage": {
                    "value": pagebody,
                    "representation": "storage"
                }
            },
        }
        response = self._post(self.rest_url + "/content/",
                              data=json.dumps(data))
        if not response.ok:
            return None
        return json.loads(response.content.decode("utf-8"))


