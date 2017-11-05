# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        ConfluenceSpace
#
# Author:      VollGaz
# -------------------------------------------------------------------------------


class ConfluenceSpace(object):
    def __init__(self, client):
        self._confluenceclient = client

    def get_spaces(self, spacetype=""):
        data = self._confluenceclient.get_spaces()
        return[u for u in data if u.get('type') == spacetype]

    def get_space_properties(self, spacekey):
        return self._confluenceclient.get_space_properties(spacekey)

    def get_space_authorized_groups(self, spacekey):
        jsonreponse = self._confluenceclient.get_space_permissions(spacekey)
        dictgroups = dict()
        for result in jsonreponse:
            for permission in result['spacePermissions']:
                if not permission['groupName'] is None and not dictgroups.__contains__(permission['groupName']):
                        dictgroups[permission['groupName']] = 0
        return dict.keys(dictgroups)
