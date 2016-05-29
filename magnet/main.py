#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from util import exec_cmd
from topology import Topology 
from extloader import load_exts, set_ext_dict_to_topology

def main(argvs):
    ext_dict = load_exts()

    topology = Topology()
    set_ext_dict_to_topology(ext_dict, topology)
    
    if len(argvs) != 3:
        print ('Usage: # python %s <topology json filepath> <COMMAND:create|delete>'
            % (argvs[0], ))
        quit()
    else:
        topo_json_filepath = argvs[1]
        command = argvs[2]

    topology.load(topo_json_filepath)
    if command == 'create':
        print 'Creating topology ... '
        topology.create()
    elif command == 'delete':
        print 'Deleting topology ... '
        topology.delete()

    #exec_cmd('sudo brctl show')
    #exec_cmd('sudo ip link')
    #exec_cmd('sudo ip netns')


if __name__ == '__main__':
    argvs = sys.argv
    main(argvs)


