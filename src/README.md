purestorage Storage Backend for Cinder
-------------------------------

Overview
========

This charm provides a Purestorage storage backend for use with the Cinder
charm.

To use:

    juju deploy cinder
    juju deploy cinder-purestorage --config driver-source="ppa:openstack-charmers/purestorage-stable"
    juju add-relation cinder-purestorage cinder

The Purestorage python packages are currently provided through a PPA which
is managed by the OpenStack Charmers team until such time as the driver
packages can be added to Ubuntu and/or the Ubuntu Cloud Archive.

Configuration
=============

See config.yaml for details of configuration options. The cinder-purestorage
charm needs to be configured to point at the storage array. Typically, the
settings that need to be configured are:

    protocol: iscsi
    volume-backend-name: cinder-pure
    san-ip: PURESTORAGE_IP
    pure-api-token: API_TOKEN

See config.yaml for the full list of configuration options.
