

import re

from utils import stringhtml
from crowd import *
from confluence import *


class ConfluenceAdmins(object):

    def __init__(self, confclient=None, crdclient=None):
        self._crowdclient = crdclient
        self._crowdgroup = CrowdGroup(client=crdclient)
        self._confluenceclient = confclient
        self._confluencecontent = ConfluenceContent(client=confclient)
        self._confluencegroup = ConfluenceGroup(client=confclient)
        self._confluencespace = ConfluenceSpace(client=confclient)

    def create_admin_summary(self, pagetitle="", pageparenttitle="", spacekey="", pagebody=""):
        self._confluencecontent.push_content(pagetitle=pagetitle,
                                             pageparenttitle=pageparenttitle,
                                             spacekey=spacekey,
                                             pagebody=pagebody)

    def generate_pagebody(self):
        htmlpage = str("")
        i = 0
        listspaces = self._confluencespace.get_spaces('global')
        for space in listspaces:
            htmlpage += "<h2>" + stringhtml(space.get('name')) + " (" + stringhtml(space.get('key')) + ")</h2>"
            listgroupsinspace = self._confluencespace.get_space_authorized_groups(space.get('key'))
            htmlpage += "<b>" + stringhtml(', '.join(map(str, listgroupsinspace))) + "</b>"
            listadminsinspace = []
            for group in listgroupsinspace:
                if re.search("-admin|-pm|_admin", group) is not None and not self.is_group_invisible(group):
                    try:
                        listadminsinspace += self._confluencegroup.get_groups_users(group)
                    except TypeError:
                        print("API de confluence non joignable")
                        try:
                            listadminsinspace += self._crowdgroup.get_group_users(group)
                        except TypeError:
                            print("API de crowd non joignable")
            htmlpage += "<ul>"
            listadminsinspace = set(listadminsinspace)
            for user in listadminsinspace:
                try:
                    userdata = self._confluenceclient.get_user(user)
                    htmlpage += "<li><p>" + stringhtml(userdata['fullname'] + ", " + userdata['name'] + ", " + userdata['email']) + "</p></li>"
                except KeyError:
                    continue
            htmlpage += "</ul>"
            i += 1
            print("Espaces traités : %d / %d" % (i, str(listspaces.__len__())))
        return htmlpage





    def is_group_invisible(self, groupname):
        listinvisiblegroup = ['jira-administrators', 'confluence-administrators', 'crowd-administrators']
        if listinvisiblegroup.__contains__(groupname):
            return True
        else:
            return False


