#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import json
import unittest

from magnet.topology import Topology
from magnet.test.utils import create_cmdexecutor

def load_json_file(json_filepath):
    obj = {}
    with open(json_filepath, 'r') as f:
        obj = json.loads(f.read())
    return obj

def load_lines(filepath):
    lines = []
    with codecs.open(filepath, 'r', 'utf-8') as f:
        lines = f.readlines()
    return lines

class TestTopology(unittest.TestCase):
    def test___init__(self):
        obj = Topology()

        self.assertIsNotNone(obj._channel_dict)
        self.assertEquals(0, len(obj._channel_dict))
        self.assertIsNotNone(obj._node_dict)
        self.assertEquals(0, len(obj._node_dict))
        self.assertIsNotNone(obj._app_factory)

    def test_append_channel(self):
        obj = Topology()
        name = 'myChannel'
        channel_obj = {
            'name': name,
        }

        obj.append_channel(channel_obj)
        self.assertEquals(1, len(obj._channel_dict))
        self.assertEquals(name, obj._channel_dict[name].get_name())

    def test_append_channel_with_opts(self):
        obj = Topology()
        name = 'myChannel'
        channel_obj = {
            'name': name,
            'opts': {
                'key1': 'value1',
                'key2': 'value2',
            },
        }

        obj.append_channel(channel_obj)
        self.assertEquals(2, len(obj._channel_dict[name]._opts))

    def test_append_node(self):
        obj = Topology()
        name = 'myNode'
        node_obj = {
            'name': name,
        }

        obj.append_node(node_obj)
        self.assertEquals(1, len(obj._node_dict))
        self.assertEquals(name, obj._node_dict[name].get_name())

    def test_append_node_with_opts(self):
        obj = Topology()
        name = 'myNode'
        node_obj = {
            'name': name,
            'opts': {
                'key1': 'value1',
                'key2': 'value2',
            },
        }

        obj.append_node(node_obj)
        self.assertEquals(2, len(obj._node_dict[name]._opts))

    def test_append_node_with_net_device_without_channel(self):
        obj = Topology()
        name = 'myNode'
        node_obj = {
            'name': name,
            'net_devices': [
                {
                    'name': 'myNetDevice1',
                },
                {
                    'name': 'myNetDevice2',
                },
            ],
        }

        obj.append_node(node_obj)
        node = obj._node_dict[name]
        self.assertEquals(2, len(node._net_devices))
        net_device = node._net_devices['myNetDevice1']
        self.assertEquals('myNetDevice1', net_device.get_name())
        net_device = node._net_devices['myNetDevice2']
        self.assertEquals('myNetDevice2', net_device.get_name())
    
    def test_append_node_with_net_device_and_channel(self):
        obj = Topology()
        channel_name = 'myChannel'
        channel_obj = {
            'name': channel_name,
        }
        node_name = 'myNode'
        node_obj = {
            'name': node_name,
            'net_devices': [
                {
                    'name': 'myNetDevice1',
                    'channel_name': channel_name,
                },
            ],
        }

        obj.append_channel(channel_obj)
        obj.append_node(node_obj)
        node = obj._node_dict[node_name]
        channel = obj._channel_dict[channel_name]
        net_device = node._net_devices['myNetDevice1']
        self.assertIsNotNone(net_device)
        self.assertEquals(channel, net_device._channel)
    
    def test_append_node_with_application(self):
        obj = Topology()
        node_name = 'myNode'
        node_obj = {
            'name': node_name,
            'applications': [
                {
                    'app_name': 'dummy',
                },
            ]
        }

        obj.append_node(node_obj)
        node = obj._node_dict[node_name]
        self.assertEquals(1, len(node._applications))
        app = node._applications[0]
        self.assertEquals(node, app._node)

    def test_setup_topology_obj(self):
        obj = Topology()
        topo_obj = load_json_file('./examples/1host-1gw/topo.json')

        obj.setup_topology_obj(topo_obj)
        self.assertEquals(1, len(obj._channel_dict))
        self.assertEquals(2, len(obj._node_dict))
        channel = obj._channel_dict['vbr-pext']
        node_qgw = obj._node_dict['qgw']
        node_qhost1 = obj._node_dict['qhost1']
        self.assertEquals(1, len(node_qgw._net_devices))
        self.assertEquals('veth0', node_qgw._net_devices['veth0'].get_name())
        self.assertEquals(channel, node_qgw._net_devices['veth0']._channel)
        self.assertEquals(1, len(node_qgw._applications))
        self.assertEquals('ip_helper', node_qgw._applications[0].get_name())
        self.assertEquals(1, len(node_qhost1._net_devices))
        self.assertEquals('veth0', node_qhost1._net_devices['veth0'].get_name())
        self.assertEquals(channel, node_qhost1._net_devices['veth0']._channel)
        self.assertEquals(1, len(node_qhost1._applications))
        self.assertEquals('ip_helper', node_qhost1._applications[0].get_name())

    def test_create(self):
        obj = Topology()
        cmdlist = []
        cmdexec = create_cmdexecutor(cmdlist)
        obj.set_cmdexecutor(cmdexec)
        topo_obj = load_json_file('./examples/1host-1gw/topo.json')
        obj.setup_topology_obj(topo_obj)

        obj.create()

        self.assertEquals(True, obj._is_created)
        expected_cmdlist = [
                line.strip() 
                for line in load_lines('./magnet/test/create.1host-1gw.sh')
                ]
        self.assertEquals(len(expected_cmdlist), len(cmdlist), cmdlist)
        for idx in range(len(expected_cmdlist)):
            self.assertEquals(expected_cmdlist[idx], cmdlist[idx])

    def test_delete(self):
        obj = Topology()
        cmdlist = []
        cmdexec = create_cmdexecutor(cmdlist)
        obj.set_cmdexecutor(cmdexec)
        topo_obj = load_json_file('./examples/1host-1gw/topo.json')
        obj.setup_topology_obj(topo_obj)

        obj.delete()

        self.assertEquals(False, obj._is_created)
        expected_cmdlist = [
                line.strip() 
                for line in load_lines('./magnet/test/delete.1host-1gw.sh')
                ]
        self.assertEquals(len(expected_cmdlist), len(cmdlist))
        for idx in range(len(expected_cmdlist)):
            self.assertEquals(expected_cmdlist[idx], cmdlist[idx])


# EOF
