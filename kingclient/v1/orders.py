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


class Order(base.Resource):
    def __repr__(self):
        return "<Order %s>" % self._info


class OrderManager(base.BaseManager):
    resource_class = Order

    def list(self):
        """Get a list of Order.

        :rtype: list of :class:`Order`
        """
        url = '/order'
        return self._list(url)

    def create(self, value):
        """Create Order.

        :rtype: class:`Order`
        """
        url = '/order'
        return self._post(url, value)
