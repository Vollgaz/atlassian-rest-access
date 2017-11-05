from jira.jiraclient import JiraClient


class JiraRole(object):

    def __init__(self, client):
        self._jiraclient = client

    def get_actors_for_role(self, projectid="", roleid=""):
        jsonresponse = self._jiraclient.get_role_agent(projectid=projectid, roleid=roleid)
        return[actor['name'] for actor in jsonresponse['actors']]
