import charms_openstack.charm

charms_openstack.charm.use_defaults('charm.default-select-release')


class CinderpurestorageCharm(
        charms_openstack.charm.CinderStoragePluginCharm):

    name = 'cinder_purestorage'
    version_package = 'python-purestorage'
    release = 'ocata'
    packages = [version_package]
    release_pkg = 'cinder-common'
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
        image_cache = []
        iscsi = []
        repl = []
        driver_options = [
            ('san_ip', self.config.get('san-ip')),
            ('pure_api_token', self.config.get('pure-api-token')),
            ('use_multipath_for_image_xfer', self.config.get('use-multipath')),
            ('image_volume_cache_enabled',
                self.config.get('use-image-cache')),
            ('pure_eradicate_on_delete',
                self.config.get('eradicate-on-delete')),
            ('pure_automatic_max_oversubscription_ratio',
                self.config.get('automatic-max-oversubscription')),
            ('volume_driver', volumedriver),
            ('volume_backend_name', service)]

        if self.config.get('protocol') == 'iscsi':
            if self.config.get('iscsi-cidr'):
                iscsi.extend([('pure_iscsi_cidr',
                             self.config.get('iscsi-cidr'))])
            if self.config.get('use-chap'):
                iscsi.extend([('use_chap_auth',
                             self.config.get('use-chap'))])

        if self.config.get('use-image-cache'):
            image_cache = [
                ('image_volume_cache_max_size_gb',
                    self.config.get('image-volume-cache-max-size-gb', 0)),
                ('image_volume_cache_max_count',
                    self.config.get('image-volume-cache-max-count', 0))]

        if self.config.get('use-replication'):
            replication_device = 'backend_id:' + \
                self.config.get('replication-target-name') + \
                ',san_ip:' + \
                self.config.get('replication-target-address') + \
                ',api_token:' + \
                self.config.get('replication-target-api-token')
            if self.config.get('replication-type') == 'sync':
                replication_device += ',type:sync'
                if self.config.get('replication-sync-uniform', False):
                    replication_device += ',uniform:true'
            repl = [('replication_device',
                    replication_device)]
            if self.config.get('replica-interval'):
                repl.extend([('pure_replica_interval_default',
                            self.config.get('replica-interval'))])
            if self.config.get('pure-replica-retention-short'):
                repl.extend([('pure_replica_retention_short_term_default',
                            self.config.get('pure-replica-retention-short'))])
            if self.config.get('replica-retention-per-day'):
                # required for pep8 max line length compliance
                TEMP_VAR = 'pure_replica_retention_long_term_per_day_default'
                repl.extend([(TEMP_VAR,
                            self.config.get('replica-retention-per-day'))])
            if self.config.get('replica-retention-long'):
                repl.extend([('pure_replica_retention_long_term_default',
                            self.config.get('replica-retention-long'))])
            if self.config.get('replication-pgname'):
                repl.extend([('pure_replication_pg_name',
                            self.config.get('replication-pgname'))])
            if self.config.get('replication-pod'):
                repl.extend([('pure_replication_pod_name',
                            self.config.get('replication-pod'))])

        final_options = driver_options + image_cache + repl + iscsi
        return final_options


class CinderpurestorageCharmRocky(CinderpurestorageCharm):

    # Rocky needs py3 packages.
    release = 'rocky'
    version_package = 'python3-purestorage'
    packages = [version_package]
