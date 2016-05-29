#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from appimpls import set_default_apps
from application import ApplicationFactory
from components import Channel, Node, NetDevice
from cmdexecutor import exec_nothing


def deobjectize(obj, constructor):
    name = obj['name']
    opts = None
    if 'opts' in obj:
        opts = obj['opts']
    else:
        opts = {}
    return constructor(name, opts)


def deobjectize_net_device(obj, node, channel_dict):
    net_device = deobjectize(obj, NetDevice)
    node.install_net_device(net_device)
    if 'channel_name' in obj:
        channel_name = obj['channel_name']
        net_device.connect_to(channel_dict[channel_name])
    return net_device


def deobjectize_application(obj, node, app_factory):
    app_name = obj['app_name']
    if 'opts' in obj:
        opts = obj['opts']
    else:
        opts = {}
    app = app_factory.create_application(app_name, opts)
    node.install_application(app)
    return app


def deobjectize_node(obj, channel_dict, app_factory):
    node = deobjectize(obj, Node)
    if 'net_devices' in obj:
        for nd_obj in obj['net_devices']:
            deobjectize_net_device(nd_obj, node, channel_dict)
    if 'applications' in obj:
        for app_obj in obj['applications']:
            deobjectize_application(app_obj, node, app_factory)
    return node


class Topology:
    def __init__(self):
        self._execc = exec_nothing
        self._channel_dict = OrderedDict()
        self._node_dict = OrderedDict()
        self._app_factory = ApplicationFactory()
        set_default_apps(self._app_factory)
        self._is_created = False

    def set_cmdexecutor(self, cmdexecutor):
        self._execc = cmdexecutor
        self._app_factory.set_cmdexecutor(cmdexecutor)

    def append_channel(self, obj):
        channel = deobjectize(obj, Channel)
        channel.set_cmdexecutor(self._execc)
        self._channel_dict[channel.get_name()] = channel
        return channel

    def append_node(self, obj):
        node = deobjectize_node(
                obj,
                self._channel_dict,
                self._app_factory)
        node.set_cmdexecutor(self._execc)
        for net_device_name, net_device in node._net_devices.iteritems():
            net_device.set_cmdexecutor(self._execc)
        self._node_dict[node.get_name()] = node
        return node

    def setup_topology_obj(self, obj):
        if 'channels' in obj:
            for channel_obj in obj['channels']:
                self.append_channel(channel_obj)
        if 'nodes' in obj:
            for node_obj in obj['nodes']:
                self.append_node(node_obj)

    def create(self):
        for name, channel in self._channel_dict.iteritems():
            channel.create()
        for name, node in self._node_dict.iteritems():
            node.create()
        self._is_created = True

    def delete(self):
        for name, node in self._node_dict.iteritems():
            node.delete()
        for name, channel in self._channel_dict.iteritems():
            channel.delete()
        self._is_created = False

if __name__ == '__main__':
    import sys
    import json
    from cmdexecutor import exec_linux_cmd
    from extloader import load_exts, set_ext_dict_to_topology
    argvs = sys.argv
    topology = Topology()
    ext_dict = load_exts()
    set_ext_dict_to_topology(ext_dict, topology)
    topology.set_cmdexecutor(exec_linux_cmd)

    if len(argvs) != 3:
        print (
            ('Usage: ' +
             '# python %s <topology json filepath> <COMMAND:create|delete>')
            % (argvs[0], ))
        quit()
    else:
        topo_json_filepath = argvs[1]
        command = argvs[2]

    with open(topo_json_filepath, 'r') as f:
        topo_obj = json.loads(f.read())

    topology.setup_topology_obj(topo_obj)
    if command == 'create':
        print 'Creating topology ... '
        topology.create()
    elif command == 'delete':
        print 'Deleting topology ... '
        topology.delete()


# EOF
