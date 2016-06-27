# Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from kingclient.openstack.common.apiclient import base


class Quota(base.Resource):
    def __repr__(self):
        return "<Service %s>" % self._info


class QuotaManager(base.BaseManager):
    resource_class = Quota

    def _list_all(self, url, response_key=None, obj_class=None, json=None):
        """List the collection.

        :param url: a partial URL, e.g., '/servers'
        :param response_key: the key to be looked up in response dictionary,
            e.g., 'servers'. If response_key is None - all response body
            will be used.
        :param obj_class: class for constructing the returned objects
            (self.resource_class will be used by default)
        :param json: data that will be encoded as JSON and passed in POST
            request (GET will be sent by default)
        """
        if json:
            body = self.client.post(url, json=json).json()
        else:
            body = self.client.get(url).json()

        if obj_class is None:
            obj_class = self.resource_class

        data = body[response_key] if response_key is not None else body

        """
        format the data like:
        {
            "volume":[
                {'user_id':'1xxx','volume_size':'1024','volume_num':4},
                {'user_id':'2xxx','volume_size':'1024','volume_num':4},
            ]
        }
        """
        resp = {}
        for key,value in data.items():
            for res in value:
                resp[key] = []
                resp[key].append(obj_class(self, res, loaded=True))
        return resp


    def _post_all(self, url, json, response_key=None, return_raw=False):
        """Create an object.

        :param url: a partial URL, e.g., '/servers'
        :param json: data that will be encoded as JSON and passed in POST
            request (GET will be sent by default)
        :param response_key: the key to be looked up in response dictionary,
            e.g., 'server'. If response_key is None - all response body
            will be used.
        :param return_raw: flag to force returning raw JSON instead of
            Python object of self.resource_class
        """
        body = self.client.post(url, json=json).json()
        data = body[response_key] if response_key is not None else body
        if return_raw:
            return data

        resp = {}
        for key,value in data.items():
            for res in value:
                resp[key] = []
                resp[key].append(self.resource_class(self, res, loaded=True))
        return resp


    def list(self):
        """Get a list of quota.

        :rtype: list of :class:`quota`
        """
        url = '/quota'
        return self._list_all(url)


    def show(self, user_id=None):
        """Get a list of quota.

        :rtype: list of :class:`quota`
        """
        url = '/quota/detail'
        body = {
            'user_id':user_id,
        }
        return self._post_all(url, body)


    def default_list(self):
        """Get the default of quota.

        :rtype: list of :class:`quota`
        """
        url = '/quota/default'
        return self._list_all(url)

