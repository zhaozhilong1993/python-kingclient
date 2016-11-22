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

ORDER_FIELDS = (
    'id',
    'resource_id',
    'account_id',
    'price_id',
    'order_status',
    'order_type'
)


def do_service_list(kc, args=None):
    '''List the King engines.'''
    services = kc.services.list()
    utils.print_list(services, SERVICES_FIELDS, sortby_index=1)


@utils.arg('--resource_id',
           type=str,
           help='the resource ID.')
@utils.arg('--price_id',
           type=str,
           help='the price ID.')
@utils.arg('account_id',
           metavar='<account_id>',
           type=str,
           help='the account ID.')
@utils.arg('--order_type',
           default='Time',
           help='the order type.')
def do_order_create(kc, args=None):
    '''Create the order.'''
    value = {"resource_id": args.resource_id,
             "price_id": args.price_id,
             "account_id": args.account_id,
             "order_type": args.order_type}
    body = {"order": value}
    order = kc.orders.create(body)
    utils.print_list(order.to_dict(), ORDER_FIELDS, sortby_index=1)


@utils.arg('user_id',
           metavar='<user_id>',
           type=str,
           help='the resource ID.')
@utils.arg('--default_level',
           default='3',
           help='the default account level.')
@utils.arg('--default_money',
           default='10',
           help='the default money.')
@utils.arg('--default_password',
           default='10',
           help='the default account password.')
def do_account_create(kc, args=None):
    '''Create the account.'''
    pass


@utils.arg('--price_type',
           type=str,
           help='The price type.We have: flavor; disk; image; floating_ip')
@utils.arg('--order_type',
           type=str,
           default='time',
           help='The order type.Default: time;'
                'Choose: time and usage.')
@utils.arg('--resource_id',
           type=str,
           default='',
           help='The relation resource id.Like flavor-id, image-id.'
                'If the resource is disk or floating_ip,'
                'resource id is not necessary.')
@utils.arg('--price_num',
           type=str,
           default='10',
           help='the default account password.')
def do_price_create(kc, args=None):
    '''Create the price template.'''
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
