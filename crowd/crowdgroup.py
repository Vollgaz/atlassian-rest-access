# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        CrowdTask
# Purpose:     Topping for crowdclient.py
#
# Author:      VollGaz
# -------------------------------------------------------------------------------


from lxml import etree


class CrowdGroup(object):
    def __init__(self, client):
        self._crowdclient = client
        self._depthRank = 0

    def map_all_group_link(self):
        """

        :return:
        """

        for group in self.get_all_groups():
            self.map_my_group_link(group)
            self._depthRank = 0

    def map_my_group_link(self, groupName):
        """ Give the groups where the given group is nested. It works recursively until there is no more nested group

        :param groupName:
        :return:
        """
        for rank in range(self._depthRank):
            print('---')
        print("-> %s:" % (groupName))
        self._depthRank += 1

        listGroupMemberShip = self._crowdclient.get_parent_groups(groupName)
        for group in listGroupMemberShip:
            self.map_my_group_link(group)
            self._depthRank -= 1


    def get_all_groups(self):
        xmlStr = self._crowdclient.get_all_membership()
        xmlBytes = bytes(bytearray(xmlStr, encoding="utf-8"))
        xml = etree.XML(xmlBytes)
        return [u.get('group') for u in xml.findall('membership')]

    def get_group_users(self, groupname):
        return self._crowdclient.get_group_users(groupname)
