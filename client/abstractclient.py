# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        AbstractClient
# Purpose:     generic class for the differents atlassian clients
#
# Author:      VollGaz
# -------------------------------------------------------------------------------

import requests


class AbstractClient(object):
    def __init__(self, url, user_name, user_pass, ssl_verify=True, timeout=None):

        self._url = url
        self._user_name = user_name
        self.timeout = timeout

        self.session = requests.Session()
        self.session.verify = ssl_verify
        self.session.auth = requests.auth.HTTPBasicAuth(user_name, user_pass)
        self._set_json_mode()

    def _set_json_mode(self):
        self.session.headers.update({
            "Content-type": "application/json",
            "Accept": "application/json"
        })

    def _set_xml_mode(self):
        self.session.headers.update({
            "Content-type": "application/xml",
            "Accept": "application/xml"
        })

    def __str__(self):
        return "%s at %s" % (self.__class__, self._url)

    def __repr__(self):
        return "<%s('%s', '%s')>" % (self.__class__.__name__, self._url, self._user_name)

    def _get(self, *args, **kwargs):
        """Wrapper around Requests for GET requests

        Returns:
            Response:
                A Requests Response object
        """

        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        req = self.session.get(*args, **kwargs)
        return req

    def _post(self, *args, **kwargs):
        """Wrapper around Requests for POST requests

        Returns:
            Response:
                A Requests Response object
        """

        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        req = self.session.post(*args, **kwargs)
        return req

    def _delete(self, *args, **kwargs):
        """Wrapper around Requests for DELETE requests

        Returns:
            Response:
                A Requests Response object
        """

        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        req = self.session.delete(*args, **kwargs)
        return req

    def _put(self, *args, **kwargs):
        """Wrapper around Requests for PUT requests

        Returns:
            Response:
                A Requests Response object
        """
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        req = self.session.put(*args, **kwargs)
        return req
