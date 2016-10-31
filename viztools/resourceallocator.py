#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=R0801

# Copyright (c) 2016, Blue Brain Project
#                     Raphael Dumusc <raphael.dumusc@epfl.ch>
#                     Daniel Nauchbaur <daniel.nauchbaur@epfl.ch>
#                     Cyrille Favreau <cyrille.favreau@epfl.ch>
#
# This file is part of VizTools
# <https://github.com/BlueBrain/VizTools>
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3.0 as published
# by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# All rights reserved. Do not distribute without further notice.

"""
The resource allocator manages sessions and jobs on the cluster
"""


import requests
import json
import viztools.settings as settings


class ResourceAllocator(object):
    """
    The resource allocator manages sessions and jobs on the cluster
    """

    def __init__(self,
                 service_url=settings.DEFAULT_ALLOCATOR_URI,
                 service_api_version=settings.DEFAULT_ALLOCATOR_API_VERSION):
        self._cookies = None
        self._url_service = service_url + '/rendering-resource-manager/' + service_api_version
        self._url_session = self._url_service + '/session/'
        self._url_config = self._url_service + '/config/'
        self._headers = {"Content-Type": "application/json"}

    def __request(self, verb, url, payload=None, action=None):
        """
        Invoke tool via HTTP REST interface
        """
        body = None
        request = None
        full_url = url
        if action is not None:
            full_url = full_url + action
        if payload is not None:
            body = json.dumps(payload)
        if verb == 'POST':
            request = requests.post(
                full_url, cookies=self._cookies, headers=self._headers, data=body)
        elif verb == 'PUT':
            request = requests.put(
                full_url, cookies=self._cookies, headers=self._headers, data=body)
        elif verb == 'DELETE':
            request = requests.delete(
                full_url, cookies=self._cookies, headers=self._headers, data=body)
        elif verb == 'GET':
            request = requests.get(
                full_url, cookies=self._cookies, headers=self._headers, data=body)
        if self._cookies is None:
            self._cookies = request.cookies
        return json.loads(request.text)

    def session_create(self, payload):
        """
        Create a session
        """
        self._cookies = None
        return self.__request('POST', self._url_session, payload)

    def session_list(self):
        """
        List existing sessions
        """
        return self.__request('GET', self._url_session)

    def session_delete(self):
        """
        Delete a session
        """
        return self.__request('DELETE', self._url_session)

    def session_schedule(self, payload):
        """
        Schedule a job
        """
        return self.__request('PUT', self._url_session, payload, 'schedule')

    def session_status(self):
        """
        Request for session status
        """
        return self.__request('GET', self._url_session, None, 'status')

    def session_log(self):
        """
        Request for session log
        """
        return self.__request('GET', self._url_session, None, 'log')

    def session_job(self):
        """
        Request for job information
        """
        return self.__request('GET', self._url_session, None, 'job')

    def session_streaming_url(self):
        """
        Request for streaming url
        """
        return self.__request('GET', self._url_session, None, 'imagefeed')

    def config_create(self, payload):
        """
        Create configuration
        """
        return self.__request('POST', self._url_config, payload)

    def config_update(self, payload):
        """
        Update configuration
        """
        return self.__request('PUT', self._url_config, payload)

    def config_list(self):
        """
        List existing configurations
        """
        return self.__request('GET', self._url_config)

    def config_delete(self, payload):
        """
        Delete configuration
        """
        return self.__request('DELETE', self._url_config, payload)
