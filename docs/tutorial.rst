Tutorial
========

Creates example topology
------------------------

To create an example topology, execute the following command.::

    $ magnet-cli create-topology --file examples/2host-2srv-1gw/topo.json 
    {"channels": [{"name": "vbr-pext", "opts": {}}, {"name": "vbr-pint",  ...
    

Shows current topology
----------------------

To show the current topology, execute the following command.::

    $ magnet-cli get-topology
    {"channels": [{"name": "vbr-pext", "opts": {}}, {"name": "vbr-pint",  ...
    

Confirms the virtual network
----------------------------

To confirm the current network topology, 'ip netns' command could be used.::

    $ ip netns 
    qhost2
    qhost1
    qsrv2
    qsrv1
    qgw
    $ sudo ip netns exec qhost1 ping -c2 qsrv1
    PING qsrv1 (192.168.131.2) 56(84) bytes of data.
    64 bytes from qsrv1 (192.168.131.2): icmp_seq=1 ttl=63 time=0.067 ms
    64 bytes from qsrv1 (192.168.131.2): icmp_seq=2 ttl=63 time=0.057 ms

    --- qsrv1 ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 999ms
    rtt min/avg/max/mdev = 0.057/0.062/0.067/0.005 ms


Deletes current topology
------------------------

To delete the current topology, execute the following commands.::

    $ magnet-cli delete-topology
    {"channels": [], "nodes": []}


