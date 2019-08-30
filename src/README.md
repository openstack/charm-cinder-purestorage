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
