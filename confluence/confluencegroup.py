# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
#
# Author:      VollGaz
# -------------------------------------------------------------------------------


class ConfluenceGroup(object):

    def __init__(self, client):
        self._confluenceclient = client

    def get_groups_users(self, groupname):
        jsonreponse = self._confluenceclient.get_group_members(groupname)
        return [user['username'] for user in jsonreponse]
