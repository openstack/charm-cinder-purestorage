# Copyright 2016 Canonical Ltd
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

import charmhelpers

import charm.openstack.cinder_purestorage as cinder_purestorage

import charms_openstack.test_utils as test_utils


class TestCinderpurestorageCharm(test_utils.PatchHelper):

    def _patch_config_and_charm(self, config):
        self.patch_object(charmhelpers.core.hookenv, 'config')

        def cf(key=None):
            if key is not None:
                return config[key]
            return config

        self.config.side_effect = cf
        c = cinder_purestorage.CinderpurestorageCharm()
        return c

    def test_cinder_base(self):
        charm = self._patch_config_and_charm({})
        self.assertEqual(charm.name, 'cinder_purestorage')
        self.assertEqual(charm.version_package, 'python-purestorage')
        self.assertEqual(charm.packages, ['python-purestorage'])

    def test_cinder_configuration(self):
        charm = self._patch_config_and_charm({'a': 'b'})
        config = charm.cinder_configuration()
        # Add check here that configuration is as expected.
        self.assertEqual(config, [('san_ip', None),
                                  ('pure_api_token', None),
                                  ('use_multipath_for_image_xfer', None),
                                  ('image_volume_cache_enabled', None),
                                  ('pure_eradicate_on_delete', None),
                                  ('pure_automatic_max_oversubscription_ratio',
                                      None),
                                  ('volume_driver', None),
                                  ('volume_backend_name', None),
                                  ('allowed_direct_url_schemes', 'cinder')])
