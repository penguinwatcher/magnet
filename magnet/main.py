#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pkg_resources
from util import exec_cmd
from topology import Topology 

def load_exts():
    func_dict = {}
    for plugin in pkg_resources.iter_entry_points('magnet_ext'):
        func = plugin.load()
        msg = 'Loading {0}'.format(plugin.name)
        print(msg)
        func_dict[plugin.name] = func
    return func_dict

def set_ext_dict_to_topology(ext_dict, topology):
    for plugin_name, func_dict in ext_dict.iteritems():
        print('Setting {0}'.format(plugin_name))
        app_impl_factory_dict = func_dict()
        for app_name, app_impl_factory in app_impl_factory_dict.iteritems():
            topology.app_factory.register_app_impl_factory(app_name, app_impl_factory)
            print('Registered {0}'.format(app_name))

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


