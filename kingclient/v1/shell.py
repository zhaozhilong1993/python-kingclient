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

SERVICES_FIELDS = (
    'hostname',
    'engine_id',
    'host',
    'topic',
    'updated_at',
    'status'
)

VOLUME_FIELDS = (
    'user_id',
    'volume_num',
    'volume_size',
    'updated_at'
)

FIELDS = {
    'services':SERVICES_FIELDS,
    'volume':VOLUME_FIELDS
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

    services = hc.services.list()
    utils.print_list(services, FIELDS['services'], sortby_index=1)


def do_quota_list(hc, args=None):
    '''List the quota info.'''
    show_deprecated('king quota-list',
                    'openstack quota list')

    quotas = hc.quota.list()
    for key,value in quotas.items():
        print utils.newline_index(key)
        utils.print_list(value, FIELDS[key], sortby_index=1)


@utils.arg('user_id',
           metavar='<user_id>',
           default=None,
           type=str,
           help='the user ID.')
def do_quota_show(hc, args=None):
    '''Show the quota info.'''
    show_deprecated('king quota-show',
                    'openstack quota show')

    quotas = hc.quota.show(args.user_id)
    for key,value in quotas.items():
        print utils.newline_index(key)
        utils.print_list(value, FIELDS[key], sortby_index=1)


def do_default_list(hc, args=None):
    '''List the default quota info.'''
    show_deprecated('king default-list',
                    'openstack quota default list')

    quotas = hc.quota.default_list()
    for key,value in quotas.items():
        print utils.newline_index(key)
        utils.print_list(value, FIELDS[key], sortby_index=1)


@utils.arg('size',
           metavar='<size>',
           type=int,
           help='Volume size, in GiBs.')
@utils.arg(
    '--snapshot-id',
    metavar='<snapshot-id>',
    default=None,
    help='Creates volume from snapshot ID. '
         'Default=None.')
@utils.arg(
    '--snapshot_id',
    help='Snapshot ID form the snapshot')
@utils.arg(
    '--source-volid',
    metavar='<source-volid>',
    default=None,
    help='Creates volume from volume ID. '
         'Default=None.')
@utils.arg(
    '--source_volid',
    help='Creates volume from volume ID. Default=None.')
@utils.arg(
    '--image-id',
    metavar='<image-id>',
    default=None,
    help='Creates volume from image ID. '
         'Default=None.')
@utils.arg(
    '--image_id',
    help='Creates volume from image ID. Default=None.')
@utils.arg(
    '--display-name',
    metavar='<display-name>',
    default=None,
    help='Volume name. '
         'Default=None.')
@utils.arg(
    '--display-description',
    metavar='<display-description>',
    default=None,
    help='Volume description. '
         'Default=None.')
@utils.arg(
    '--display_description',
    help='Volume description. Default=None.')
@utils.arg(
    '--volume-type',
    metavar='<volume-type>',
    default=None,
    help='Volume type. '
         'Default=None.')
@utils.arg(
    '--volume_type',
    help='Volume type. Default=None.')
@utils.arg(
    '--availability-zone',
    metavar='<availability-zone>',
    default=None,
    help='Availability zone for volume. '
         'Default=None.')
@utils.arg(
    '--availability_zone',
    help='Availability zone for volume. Default=None.')
@utils.arg('--metadata',
           type=str,
           nargs='*',
           metavar='<key=value>',
           default=None,
           help='Metadata key and value pairs. '
                'Default=None.')
@utils.service_type('volume')
def do_volumes_create(hc, args):
    """Creates a volumes."""
    field = ('id','name')
    volume_metadata = None
    if args.metadata is not None:
        volume_metadata = _extract_metadata(args)

    volume = hc.volume.create(args.size,
                              args.snapshot_id,
                              args.source_volid,
                              args.display_name,
                              args.display_description,
                              args.volume_type,
                              availability_zone=args.availability_zone,
                              imageRef=args.image_id,
                              metadata=volume_metadata)
    for key,value in volume.items():
        utils.print_list(value, field, sortby_index=1)


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

