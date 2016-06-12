Developer's guide
=================

Supported platform and prerequisites
------------------------------------

See :doc:`Installation`

Preparation
-----------

Install git.::

    $ sudo apt-get install git-core -y

Install pip.::

    $ curl -O curl -O https://bootstrap.pypa.io/get-pip.py
    ...
    $ sudo python get-pip.py

To remove pip warning, create cache directory.::

    $ mkdir -p ~/.cache/pip/http

To develop magnet, it is useful to use virtualenv.::

    $ sudo pip install virtualenv

Flake8 should be installed.::

    $ sudo pip install flake8


Installation
------------

Clone magnet from github.::

    $ git clone https://github.com/penguinwatcher/magnet.git

Create a virtualenv for magnet.::

    $ virtualenv magnet-env

Install magnet to the virtualenv.::

    $ cd magnet
    $ source ../magnet-env/bin/activate
    (magnet-env) $ pip install -e .

How to start and stop magnet
----------------------------

To start magnet service, execute the following command.::

    (magnet-env) $ sudo ../magnet-env/bin/magnet

NOTICE: 'sudo' is required because magnet internally uses brctl, ip netns and so on.

To stop magnet service, open another console, and then execute the following command.::

    (magnet-env) $ sudo pkill -f magnet


Direct topology operation for debugging
---------------------------------------

To create a network topology, execute the following command.::

    $ sudo python magnet/topology.py ./examples/1host-1gw/topo.json create

To verify the result, execute the following command.::

    $ sudo ip netns exec qhost1 ping -c2 qgw

To delete the network topology, execute the following command.::

    $ sudo python magnet/topology.py ./examples/1host-1gw/topo.json delete


