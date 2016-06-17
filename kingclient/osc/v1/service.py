#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Orchestration v1 Service action implementations"""

import logging

from cliff import lister
from openstackclient.common import utils


class ListService(lister.Lister):
    """List the Heat engines."""

    log = logging.getLogger(__name__ + ".ListService")

    def get_parser(self, prog_name):
        parser = super(ListService, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        king_client = self.app.client_manager.orchestration
        columns = ['hostname', 'binary', 'engine_id', 'host',
                   'topic', 'updated_at', 'status']
        services = king_client.services.list()
        return (
            columns,
            (utils.get_item_properties(s, columns) for s in services)
        )
