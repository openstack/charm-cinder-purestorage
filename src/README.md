purestorage Storage Backend for Cinder
-------------------------------

Overview
========

This charm provides a purestorage storage backend for use with the Cinder
charm.

To use:

    juju deploy cinder
    juju deploy cinder-purestorage --config driver-source="ppa:narindergupta/purestorage"
    juju add-relation cinder-purestorage cinder

Until purestorage packages went into Canonical repository plese use the driver
source from PPA narindergupta/purestorage.

Configuration
=============

See config.yaml for details of configuration options.
The cinder-purestorage charm needs to be configured to point the storage array.
Typically the settings that need configuring are:

    protocol: iscsi
    volume-backend-name: cinder-pure
    san-ip: PURESTORAGE_IP
    pure-api-token: API_TOKEN

See config.yaml for full list of configuration options.
