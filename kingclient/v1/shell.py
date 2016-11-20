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

from kingclient.common import utils

logger = logging.getLogger(__name__)

SERVICES_FIELDS = (
    'hostname',
    'engine_id',
    'host',
    'topic',
    'updated_at',
    'status'
)


def do_service_list(hc, args=None):
    '''List the King engines.'''
    services = hc.services.list()
    utils.print_list(services, SERVICES_FIELDS, sortby_index=1)


@utils.arg('resource_id',
           metavar='<resource_id>',
           type=str,
           help='the resource ID.')
@utils.arg('price_id',
           metavar='<price_id>',
           type=str,
           help='the price ID.')
@utils.arg('account_id',
           metavar='<account_id>',
           type=str,
           help='the account ID.')
@utils.arg('order_type',
           metavar='<order_type>',
           default='Time',
           type=str,
           help='the account ID.')
def do_order_create(hc, args=None):
    '''Create the order.'''
    pass


def _extract_metadata(args):
    metadata = {}
    for metadatum in args.metadata:
        # unset doesn't require a val, so we have the if/else
        if '=' in metadatum:
            (key, value) = metadatum.split('=', 1)
        else:
            key = metadatum
            value = None

        metadata[key] = value
    return metadata
