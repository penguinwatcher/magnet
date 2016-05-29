#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pkg_resources
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

if __name__ == '__main__':
    pass


