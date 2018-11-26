import charms_openstack.charm as charm
import charms.reactive as reactive


import charm.openstack.cinder_purestorage as cinder_pure
assert cinder_pure


@reactive.when_any('install')
def install_pure_driver():
    with charm.provide_charm_instance() as charm_class:
        charm_class.install()


@reactive.when('storage-backend.available')
@reactive.when_not('cinder.configured')
def storage_backend(principle):
    with charm.provide_charm_instance() as charm_class:
        name, config = charm_class.get_purestorage_config()
        principle.configure_principal(name, config)
    reactive.set_state('cinder.configured')


@reactive.hook('config-changed')
def update_config():
    reactive.remove_state('cinder.configured')
