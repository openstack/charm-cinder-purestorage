# Copyright 2019
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import charms_openstack.charm
import charms.reactive

# This charm's library contains all of the handler code associated with
# this charm -- we will use the auto-discovery feature of charms.openstack
# to get the definitions for the charm.
import charms_openstack.bus
charms_openstack.bus.discover()

charms_openstack.charm.use_defaults(
    'charm.installed',
    'update-status',
    'upgrade-charm',
    'storage-backend.connected',
)


@charms.reactive.when('config.changed.driver-source')
def reinstall():
    with charms_openstack.charm.provide_charm_instance() as purestorage:
        purestorage.install()
