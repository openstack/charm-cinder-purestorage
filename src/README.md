Pure Storage Backend for Cinder
-------------------------------

Overview
========

This charm provides a Pure Storage backend for use with the Cinder
charm.

To use:

    juju deploy cinder
    juju deploy -n 3 ceph
    juju deploy cinder-purestorage
    juju add-relation cinder-purestorage cinder
