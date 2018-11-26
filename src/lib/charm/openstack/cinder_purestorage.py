import json
import subprocess

from charmhelpers.core.hookenv import (
    config,
    log,
    relation_ids,
    relation_set,
    status_set,
    service_name
)

from charmhelpers.contrib.openstack.context import OSContextGenerator
from charms_openstack.charm import OpenStackCharm


class ProtocolNotImplimented(Exception):
    """Unsupported protocol error."""


class PureStorageCharm(OpenStackCharm):
    service_name = 'cinder-purestorage'
    name = 'purestorage'
    packages = ['']
    release = 'queens'

    def install(self):
        subprocess.check_call(['pip', 'install', 'purestorage', '--no-deps'])

    def get_purestorage_config(self):
        status_set('active', 'Unit is ready')
        name = config('volume-backend-name') or service_name()
        return name, PureStorageSubordinateContext()()


class PureStorageSubordinateContext(OSContextGenerator):
    interfaces = ['storage-backend']

    def __call__(self):
        log('Generating cinder.conf stanza')
        ctxt = []
        drivers = {
            'iscsi': 'cinder.volume.drivers.pure.PureISCSIDriver',
            'fc': 'cinder.volume.drivers.pure.PureFCIDriver',
        }
        service = config('volume-backend-name') or service_name()

        ctxt.append(('volume_backend_name', service))
        ctxt.append(('san_ip', config('san-ip')))
        ctxt.append(('pure_api_token', config('pure-api-token')))
        try:
            ctxt.append(
                ('volume_driver', drivers[config('protocol').lower()]))
        except KeyError:
            raise ProtocolNotImplimented(
                config('protocol'), ' is not an implimented protocol  driver, '
                'please choose between `iscsi` and `fc`.')
        return {
            "cinder": {
                "/etc/cinder/cinder.conf": {
                    "sections": {
                        service: ctxt
                    }
                }
            }
        }
