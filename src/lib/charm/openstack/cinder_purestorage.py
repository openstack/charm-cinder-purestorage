import charms_openstack.charm
import charmhelpers.core.hookenv as ch_hookenv  # noqa

charms_openstack.charm.use_defaults('charm.default-select-release')


class CinderpurestorageCharm(
        charms_openstack.charm.CinderStoragePluginCharm):

    name = 'cinder_purestorage'
    version_package = 'python-purestorage'
    release = 'ocata'
    packages = [version_package]
    stateless = True
    # Specify any config that the user *must* set.
    mandatory_config = [
        'san-ip', 'pure-api-token', 'protocol', 'volume-backend-name']

    def cinder_configuration(self):
        drivers = {
            'iscsi': 'cinder.volume.drivers.pure.PureISCSIDriver',
            'fc': 'cinder.volume.drivers.pure.PureFCDriver',
        }
        service = self.config.get('volume-backend-name')
        volumedriver = drivers.get(self.config.get('protocol'))
        driver_options = [
            ('san_ip', self.config.get('san-ip')),
            ('pure_api_token', self.config.get('pure-api-token')),
            ('volume_driver', volumedriver),
            ('volume_backend_name', service)]
        return driver_options


class CinderpurestorageCharmRocky(CinderpurestorageCharm):

    # Rocky needs py3 packages.
    release = 'rocky'
    version_package = 'python3-purestorage'
    packages = [version_package]
