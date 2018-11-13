import json

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

    def set_relation_data(self):
        rel_id = relation_ids('storage-backend')
        if not len(rel_id):
            log("No 'storage-backend' relation detected, skipping.")
        else:
            relation_set(
                relation_id=rel_id[0],
                backend_name=config()['volume-backend-name'] or service_name(),
                subordinate_configuration=json.dumps(
                    PureStorageSubordinateContext()()),
                stateless=True,
            )
            log('Relation data set for {}'.format(rel_id[0]))
        status_set('active', 'Unit is ready')


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

        for rid in relation_ids(self.interfaces[0]):
            log('Setting relation data for {}'.format(rid))
            self.related = True
            return {
                "cinder": {
                    "/etc/cinder/cinder.conf": {
                        "sections": {
                            service: ctxt
                        }
                    }
                }
            }
