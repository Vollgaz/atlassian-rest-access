from utils.utils import stringhtml
from confluence import *


class JiraAdmins(object):

    def __init__(self, jiraclient=None, confclient=None):
        self._jiraclient = jiraclient
        self._confluenceclient = confclient
        self._confluencecontent = ConfluenceContent(client=confclient)

    def create_admin_summary(self, pagetitle="", pageparenttitle="", spacekey="", pagebody=""):
        self._confluencecontent.push_content(pagetitle=pagetitle,
                                             pageparenttitle=pageparenttitle,
                                             spacekey=spacekey,
                                             pagebody=pagebody)

    def generate_page_body(self):
        listprojects = self._jiraclient.get_projects(expand='lead')
        htmlpage = str("")
        i = 0
        for project in listprojects:
            htmlpage += "<h2>" + stringhtml(project['name']) + " (" + stringhtml(project['key']) + ")</h2>"
            jsonprojectleader = self._jiraclient.get_user(username=project['lead']['name'])
            htmlpage += "<b>" + stringhtml(jsonprojectleader['displayName'] + ",  " + jsonprojectleader['name'])
            try:
                htmlpage += ",  " + stringhtml(jsonprojectleader['emailAddress'])
            except KeyError:
                pass
            finally:
                htmlpage += "</b>"
            listroles = self._jiraclient.get_project_roles(projectid=project['id'])
            htmlpage += "<ul>"
            for key, value in listroles.items():
                jsonrole = self._jiraclient.execute_request(request=value)
                listactors = [actor['name'] for actor in jsonrole['actors']]
                if len(listactors) != 0:
                    htmlpage += "<li><p>" + stringhtml(key) + " : " + stringhtml(', '.join(map(str, listactors))) + "</p></li>"
            htmlpage += "</ul>"
            i += 1
            print("Projets traités : %d / %d" % (i, listprojects.__len__()))
        return htmlpage
