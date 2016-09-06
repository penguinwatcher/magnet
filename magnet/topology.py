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


def objectize_component(component):
    obj = OrderedDict()
    obj['name'] = component._name
    obj['opts'] = component._opts
    return obj


def objectize_channel(channel):
    obj = objectize_component(channel)
    return obj


def objectize_net_device(net_device):
    obj = objectize_component(net_device)
    if net_device._channel is not None:
        obj['channel_name'] = net_device._channel._name
    return obj


def objectize_application(application):
    obj = OrderedDict()
    obj['app_name'] = application._name
    obj['opts'] = application._opts
    return obj


def objectize_node(node):
    obj = objectize_component(node)
    obj['net_devices'] = [
        objectize_net_device(net_device)
        for net_device in node._net_devices.values()]
    obj['applications'] = [
        objectize_application(application)
        for application in node._applications]
    return obj


class TopologyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


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

    def is_created(self):
        return self._is_created

    def to_obj(self):
        channels = [
                objectize_channel(channel)
                for channel in self._channel_dict.values()]
        nodes = [
                objectize_node(node)
                for node in self._node_dict.values()]
        obj = OrderedDict()
        obj['channels'] = channels
        obj['nodes'] = nodes
        return obj

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

    def check_obj(self, obj):
        if obj is None:
            raise TopologyError(
                    'Invalid argument. obj is None.')
        elif 'name' not in obj:
            raise TopologyError(
                    'Invalid argument. \'name\' not in obj.')

    def setup_topology_obj(self, obj):
        self._channel_dict.clear()
        self._node_dict.clear()
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
        self._node_dict.clear()
        self._channel_dict.clear()
        self._is_created = False

    def get_channels(self):
        obj = [
                objectize_channel(channel)
                for channel in self._channel_dict.values()]
        return obj

    def get_channel(self, name):
        obj = None
        channel = self._channel_dict[name]
        if channel is not None:
            obj = objectize_channel(channel)
        return obj

    def create_channel(self, obj):
        self.check_obj(obj)
        name = obj['name']
        if name in self._channel_dict:
            raise TopologyError(
                    'Channel already exists: %s' % name)
        channel = self.append_channel(obj)
        if channel is None:
            raise TopologyError('Internal error.')
        channel.create()
        return objectize_channel(channel)

    def update_channel(self, obj):
        self.check_obj(obj)
        name = obj['name']
        self.delete_channel(name)
        return self.create_channel(obj)

    def delete_channel(self, name):
        if name not in self._channel_dict:
            raise TopologyError(
                    'Channel not found.: %s' % name)
        channel = self._channel_dict.pop(name)
        channel.delete()
        return objectize_channel(channel)

    def get_nodes(self):
        obj = [
                objectize_node(node)
                for node in self._node_dict.values()]
        return obj

    def get_node(self, name):
        obj = None
        node = self._node_dict[name]
        if node is not None:
            obj = objectize_node(node)
        return obj

    def create_node(self, obj):
        self.check_obj(obj)
        name = obj['name']
        if name in self._node_dict:
            raise TopologyError(
                    'Node already exists: %s' % name)
        node = self.append_node(obj)
        if node is None:
            raise TopologyError('Internal error.')
        node.create()
        return objectize_node(node)

    def update_node(self, obj):
        self.check_obj(obj)
        name = obj['name']
        self.delete_node(name)
        return self.create_node(obj)

    def delete_node(self, name):
        if name not in self._node_dict:
            raise TopologyError(
                    'Node not found.: %s' % name)
        node = self._node_dict.pop(name)
        node.delete()
        return objectize_node(node)


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
