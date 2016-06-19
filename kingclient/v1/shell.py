# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from oslo_serialization import jsonutils
from oslo_utils import strutils
import six
from six.moves.urllib import request
import sys
import yaml

from kingclient.common import utils

from kingclient.openstack.common._i18n import _
from kingclient.openstack.common._i18n import _LI
from kingclient.openstack.common._i18n import _LW

import kingclient.exc as exc

logger = logging.getLogger(__name__)



VOLUME_FIELDS = (
    'user_id',
    'volume_num',
    'volume_size',
    'updated_at'
)

FIELDS = {
    'volume':VOLUME_FIELDS,
}

def show_deprecated(deprecated, recommended):
    logger.warning(_LW('"%(old)s" is deprecated, '
                    'please use "%(new)s" instead'),
                        {'old': deprecated,
                        'new': recommended}
                    )


def do_service_list(hc, args=None):
    '''List the King engines.'''
    show_deprecated('king service-list',
                    'openstack quota service list')

    fields = ['hostname', 'engine_id', 'host',
              'topic', 'updated_at', 'status']
    services = hc.services.list()
    utils.print_list(services, fields, sortby_index=1)


def do_quota_list(hc, args=None):
    '''List the quota info.'''
    show_deprecated('king quota-list',
                    'openstack quota list')

    quotas = hc.quota.list()
    for key,value in quotas.items():
        print utils.newline_index(key)
        utils.print_list(value, FIELDS[key], sortby_index=1)
