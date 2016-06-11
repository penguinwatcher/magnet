magnet
======
(no description yet)

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

Trial
-----
To create a network topology, executes the following command.

    $ sudo python magnet/topology.py ./examples/1host-1gw/topo.json create

To verify the result, executes the following command.

    $ sudo ip netns exec qhost1 ping -c2 qgw

To delete the network topology, executes the following command.

    $ sudo python magnet/topology.py ./examples/1host-1gw/topo.json delete

