import json

from client.abstractclient import AbstractClient


class JiraClient(AbstractClient):
    def __init__(self, jira_url, user_name, user_pass, ssl_verify=True, timeout=None):
        super(self.__class__, self).__init__(jira_url, user_name, user_pass, ssl_verify=ssl_verify, timeout=timeout)
        self._rest_url = self._url.rstrip("/") + "/rest/api/2"


    #Project request
    def get_projects(self, expand=""):
        self._set_json_mode()
        response = self._get(self._rest_url + '/project',
                             params={'expand': expand})
        if not response.ok:
            return None
        return json.loads(response.content.decode('UTF-8'))

    def get_project_roles(self, projectid=""):
        self._set_json_mode()
        response = self._get(self._rest_url + '/project/' + projectid + '/role')
        if not response.ok:
            return None
        return json.loads(response.content.decode('utf-8'))

    #Role request
    def get_role_agent(self, projectid="", roleid=""):
        self._set_json_mode()
        response = self._get(self._rest_url + '/project/' + projectid + '/role/' + roleid)

        if not response.ok:
            return None
        return json.loads(response.content.decode('utf-8'))

    #User request
    def get_user(self, username=""):
        self._set_json_mode()
        response = self._get(self._rest_url + '/user',
                             params={'username': username})
        if not response.ok:
            return None
        return json.loads(response.content.decode('utf-8'))

    #Specific cause jira answer contain url to other generate other request in order to get data.
    def execute_request(self, request=""):
        self._set_json_mode()
        response = self._get(request)

        if not response.ok:
            return None
        return json.loads(response.content.decode('utf-8'))

