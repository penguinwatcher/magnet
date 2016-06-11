Installation
============

Supported platform
------------------

- CPU architecture: x64
- Memory: 384MB or more
- HDD space: 8GB or more.
- Operating system: Ubuntu Server 14.04 LTS (Trusty Tahr)

Prerequisites
-------------

The following software is required.

- python v2.7
- bridge-utils
- iproute2

The following python modules are required.

- tornado 4.3

Preparation
-----------

Install required software.::

    $ sudo apt-get install bridge-utils

Installation
------------

Clone magnet from github.::

    $ git clone https://github.com/penguinwatcher/magnet.git

To install magnet, execute as follows::

    $ cd magnet
    $ sudo python setup.py install

