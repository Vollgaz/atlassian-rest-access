# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        CrowdClient
# Purpose:     Access directly the exposed confluence rpc and rest api
#
# Author:      VollGaz
# -------------------------------------------------------------------------------

import json

from client.abstractclient import AbstractClient


class CrowdClient(AbstractClient):
    def __init__(self, crowd_url, user_name, user_pass, ssl_verify=True, timeout=None):
        super(self.__class__, self).__init__(crowd_url, user_name, user_pass, ssl_verify=ssl_verify, timeout=timeout)
        self._rest_url = self._url.rstrip("/") + "/rest/usermanagement/1"

    # -----------------------------------------------------------------------------
    # Section : User
    #
    # Dedicated to the manipulation of users (create, delete, disable, ...)
    # -------------------------------------------------------------------------------


    def get_session(self, username, password, remote="127.0.0.1"):
        """Create a session for a user.

        Attempts to create a user session on the Crowd server.

        Args:
            username: The account username.

            password: The account password.

            remote:
                The remote address of the user. This can be used
                to create multiple concurrent sessions for a user.
                The host you run this program on may need to be configured
                in Crowd as a trusted proxy for this to work.

        Returns:
            dict:
                A dict mapping of user attributes if the application
                authentication was successful. See the Crowd
                documentation for the authoritative list of attributes.

            None: If authentication failed.
        """

        params = {
            "username": username,
            "password": password,
            "validation-factors": {
                "validationFactors": [
                    {"name": "remote_address", "value": remote,}
                ]
            }
        }
        response = self._post(self._rest_url + "/session",
                              data=json.dumps(params),
                              params={"expand": "user"})

        # If authentication failed for any reason return None
        if not response.ok:
            return None

        # Otherwise return the user object
        return response.json()



    def add_user(self, username, **kwargs):
        """Add a user to the directory

        Args:
            username: The account username
            **kwargs: key-value pairs:
                          password: mandatory
                          email: mandatory
                          first_name: optional
                          last_name: optional
                          display_name: optional
                          active: optional (default True)

        Returns:
            True: Succeeded
            False: If unsuccessful
        """
        # Check that mandatory elements have been provided
        if 'password' not in kwargs:
            raise ValueError("missing password")
        if 'email' not in kwargs:
            raise ValueError("missing email")

        # Populate data with default and mandatory values.
        # A KeyError means a mandatory value was not provided,
        # so raise a ValueError indicating bad args.
        try:
            data = {
                "name": username,
                "first-name": username,
                "last-name": username,
                "display-name": username,
                "email": kwargs["email"],
                "password": {"value": kwargs["password"]},
                "active": True
            }
        except KeyError:
            return ValueError

        # Remove special case 'password'
        del (kwargs["password"])

        # Put values from kwargs into data
        for k, v in kwargs.items():
            new_k = k.replace("_", "-")
            if new_k not in data:
                raise ValueError("invalid argument %s" % k)
            data[new_k] = v

        response = self._post(self._rest_url + "/user",
                              data=json.dumps(data))

        return response.status_code == 201

    def delete_user(self, username):
        """Delete a user from crowd. This functionnality should not be regulary used.

        Args:
            username:   the username to delete

        Returns:
            bool:
                True if the user successfully deleted
        """
        response = self._delete(self._rest_url + '/user',
                                params={"username": username})
        return response.status_code == 204

    def reset_user_password(self, username):
        """Send a link to a user to reset his password

        Returns:
            True: Succeeded
            False: If unsuccessful
        """

        response = self._post(self._rest_url + "/user/mail/password",
                              params={"username": username})

        return response.status_code == 204

    def get_user(self, username):
        """Retrieve information about a user

        Returns:
            dict: User information

            None: If no user or failure occurred
        """

        response = self._get(self._rest_url + "/user",
                             params={"username": username,
                                     "expand": "attributes"})
        if not response.ok:
            return None

        return response.json()

    def user_exists(self, username):
        """Determines if the user exists.

        Args:
            username: The user name.

        Returns:
            bool:
                True if the user exists in the Crowd application.
        """
        response = self._get(self._rest_url + "/user",
                             params={"username": username})

        if not response.ok:
            return None

        return True

    def add_user_to_group(self, username, groupname):
        """Add the user to the given group

        Args:
            username: The user name.
            groupname: the name of the group

        Returns:
            bool:
                True if the user been added successfully to the group
        """
        data = {"name": groupname}
        response = self._post(self._rest_url + "/user/group/direct",
                              params={"username": username},
                              data=json.dumps(data))

        return response.status_code == 201 or response.status_code == 409

    def is_direct_member(self, username, groupname):
        """Test if the user is a direct member of the given group

        Args:
            username:   the name of the user to test
            groupname:  the group where the user should be

        Returns:
            bool:
                True if the user is a direct member of the group, False otherwise
        """
        response = self._get(self._rest_url + '/group/user/direct',
                             params={'groupname': groupname, 'username': username})
        return response.status_code == 200

    def remove_user_membership(self, username, groupname):
        """Remove the user membership

        Args:
            username:   the username of the user to remove
            groupname:  the group name of the parent group

        Returns:
            bool:
                True if the user successfully removed from group
        """
        response = self._delete(self._rest_url + '/group/user/direct',
                                params={"groupname": groupname, "username": username})

        return response.status_code == 204

    def disable_user(self, username):
        """Disable a user.

        Args:
            username:   the username to disable

        Returns:
            bool:
                True if the user successfully disabled
        """

        user = self.get_user(username)
        if user:
            del (user['password'])
            user['active'] = False
            response = self._put(self._rest_url + '/user',
                                 params={'username': username},
                                 data=json.dumps(user))

            return response.status_code == 204
        else:
            return None

    def enable_user(self, username):
        """Enable a user.

        Args:
            username:   the username to enable

        Returns:
            bool:
                True if the user successfully enabled
        """

        user = self.get_user(username)
        if user:
            del (user['password'])
            user['active'] = True
            response = self._put(self._rest_url + '/user',
                                 params={'username': username},
                                 data=json.dumps(user))

            return response.status_code == 204
        else:
            return None

    def search_users(self, restriction):
        """Search a user with the given dict restrictions

        Args:
            restriction:    String containing the restriction as CQL format

        Returns:
            list:   list of usernames
        """

        response = self._get(self._rest_url + '/search',
                             params={
                                 'entity-type': 'user',
                                 'expand': 'user',
                                 'restriction': restriction
                             })
        if not response.ok:
            return None

        return response.json()['users']

    def get_user_attributes(self, username):
        """Return the list of attributes for the given user

        Args:
            username:    Username of the user

        Returns:
            list:   list of dict attributes
            None:   If user not found or error
        """
        response = self._get(self._rest_url + '/user/attribute',
                             params={'username': username})

        if not response.ok:
            return None
        return response.json()['attributes']

    # ----------------------------------------------------------------------
    # Section : Groups
    #
    # Dedicated to the manipulation of groups (create, delete, disable, ...)
    # -------------------------------------------------------------------------

    def add_group(self, group, description=None):
        """Add a group to the directory.

        Args:
            group: The group name
            description:    The group description

        Returns:
            True: Succeeded
            False: If unsuccessful
        """
        if not description:
            description = ''
        data = {
            "name": group,
            "type": 'GROUP',
            "description": description,
            "active": True
        }

        response = self._post(self._rest_url + '/group',
                              data=json.dumps(data))
        return response.status_code == 201

    def get_group(self, groupname):
        """Retrieve information about a group with its attributes

        Returns:
            dict: Group information

            None: If no group or failure occurred
        """

        response = self._get(self._rest_url + "/group",
                             params={"groupname": groupname,
                                     "expand": "attributes"})
        if not response.ok:
            return None

        return response.json()

    def get_groups(self, username):
        """Retrieves a list of group names that have <username> as a direct member.

        Returns:
            list:
                A list of strings of group names.
        """

        response = self._get(self._rest_url + "/user/group/direct",
                             params={"username": username})

        if not response.ok:
            return None

        return [g['name'] for g in response.json()['groups']]

    def get_nested_groups(self, username):
        """Retrieve a list of all group names that have <username> as a direct or indirect member.

        Args:
            username: The account username.


        Returns:
            list:
                A list of strings of group names.
        """

        response = self._get(self._rest_url + "/user/group/nested",
                             params={"username": username})

        if not response.ok:
            return None

        return [g['name'] for g in response.json()['groups']]

    def get_group_users(self, groupname):
        """Retrieves a list of all users that directly belong to the given groupname.

        Args:
            groupname: The group name.

        Returns:
            list:
                A list of strings of user names.
        """
        response = self._get(self._rest_url + "/group/user/direct",
                             params={"groupname": groupname,
                                     "start-index": 0,
                                     "max-results": 99999})
        if not response.ok:
            return None

        return [u['name'] for u in response.json()['users']]

    def get_nested_group_users(self, groupname):
        """Retrieves a list of all users that directly or indirectly belong to the given groupname.

        Args:
            groupname: The group name.

        Returns:
            list:
                A list of strings of user names.
        """
        response = self._get(self._rest_url + "/group/user/nested",
                             params={"groupname": groupname,
                                     "start-index": 0,
                                     "max-results": 99999})
        if not response.ok:
            return None
        return [u['name'] for u in response.json()['users']]

    def group_exists(self, groupname):
        """Determines if the group exists.

        Args:
            groupname: The group name.
        Returns:
            bool:
                True if the group exists in the Crowd application.
        """
        response = self._get(self._rest_url + "/group",
                             params={"groupname": groupname})
        return response.status_code == 200

    def add_group_to_group(self, group, parentgroup):
        """Add a group item to a group

        Args:
            group:   the group name to add
            parentgroup:  the parent group where the item will be added

        Returns:
            bool:
                True if the item group been added successfully to the parentgroup
        """
        data = {"name": parentgroup}
        response = self._post(self._rest_url + '/group/parent-group/direct',
                              params={"groupname": group},
                              data=json.dumps(data))

        return response.status_code == 201

    def is_group_direct_member(self, groupname, parentgroup):
        """Test if the group is a direct member of the parent group

        Args:
            groupname:   the name of the group to test
            parentgroup:  the group where the group should be

        Returns:
            bool:
                True if the group is a direct member of the parent group, False otherwise
        """
        response = self._get(self._rest_url + '/group/parent-group/direct',
                             params={'groupname': groupname, 'parent-groupname': parentgroup})
        return response.status_code == 200

    def remove_group_membership(self, groupname, parentgroup):
        """Remove the group membership

        Args:
            groupname:   the group name of the group to remove
            parentgroup:  the group name of the parent group

        Returns:
            bool:
                True if the group successfully removed from group
        """
        response = self._delete(self._rest_url + '/group/child-group/direct',
                                params={"groupname": parentgroup, "child-groupname": groupname})

        return response.status_code == 204

    def delete_group(self, groupname):
        """Delete a group from crowd. This functionnality should not be regulary used.

        Args:
            groupname:   the group to delete

        Returns:
            bool:
                True if the group successfully deleted
        """
        response = self._delete(self._rest_url + '/group',
                                params={"groupname": groupname})
        return response.status_code == 204

    def get_parent_groups(self, groupname):
        """Find groups where groupname is nested

        Args:
            groupname:   the group looking for his parents


        Returns:
            list: list of all the groups where groupname is nested
        """

        response = self._get(self._rest_url + '/group/parent-group/nested',
                             params={'groupname': groupname})

        if not response.ok:
            return None
        return [g['name'] for g in response.json()['groups']]

    def get_all_membership(self):
        """Retrieves full details of all groups membership with users and nested groups.

        Returns:
            str:
                The xml string representation of the membership list.
        """
        self._set_xml_mode()
        response = self._get(self._rest_url + "/group/membership")
        self._set_json_mode()
        if not response.ok:
            return None
        return response.content.decode('utf-8')
