#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import unittest

from magnet.components import Channel, NetDevice, Node
from magnet.application import Application, ApplicationImplementationBase
from magnet.test.dummyapplicationimpl import DummyApplicationImpl
from magnet.test.utils import create_cmdexecutor


class TestChannel(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test___init___without_opts(self):
        obj = Channel('myChannel')
        self.assertIsNotNone(obj)
        self.assertEquals('myChannel', obj._name)
        self.assertIsNotNone(obj._opts)
        self.assertEquals(0, len(obj._opts))
        self.assertEquals(0, len(obj._net_devices))

    def test___init___with_opts(self):
        opts = {'aaa':'bbb'}
        obj = Channel('myChannel', opts)
        self.assertIsNotNone(obj)
        self.assertEquals('myChannel', obj._name)
        self.assertIsNotNone(obj._opts)
        self.assertEquals(1, len(obj._opts))
        self.assertEquals(0, len(obj._net_devices))

    def test_create(self):
        cmdlist = []
        obj = Channel('myChannel')
        obj.set_cmdexecutor(create_cmdexecutor(cmdlist))

        obj.create()

        self.assertEquals(3, len(cmdlist))
        self.assertEquals('brctl addbr myChannel', cmdlist[0])
        self.assertEquals('brctl stp myChannel off', cmdlist[1])
        self.assertEquals('ip link set dev myChannel up', cmdlist[2])

    def test_delete(self):
        cmdlist = []
        obj = Channel('myChannel')
        obj.set_cmdexecutor(create_cmdexecutor(cmdlist))

        obj.delete()

        self.assertEquals(2, len(cmdlist))
        self.assertEquals('ip link set dev myChannel down', cmdlist[0])
        self.assertEquals('brctl delbr myChannel', cmdlist[1])

    def test_append_and_remove_net_device(self):
        obj = Channel('myChannel')
        net_dev = NetDevice('myNetDevice')

        self.assertEquals(0, len(obj._net_devices))

        obj.append_net_device(net_dev)
        self.assertEquals(1, len(obj._net_devices))
        self.assertEquals('myNetDevice', obj._net_devices[0]._name)

        obj.remove_net_device(net_dev)
        self.assertEquals(0, len(obj._net_devices))


class TestNetDevice(unittest.TestCase):
    def test___init___without_opts(self):
        obj = NetDevice('myNetDevice')
        self.assertIsNotNone(obj)
        self.assertEquals('myNetDevice', obj._name)
        self.assertEquals(0, len(obj._opts))
        self.assertIsNone(obj._node)
        self.assertIsNone(obj._channel)

    def test___init___with_opts(self):
        opts = {'aaa':'bbb'}
        obj = NetDevice('myNetDevice', opts)
        self.assertIsNotNone(obj)
        self.assertEquals('myNetDevice', obj._name)
        self.assertEquals(1, len(obj._opts))
        self.assertEquals('bbb', obj._opts['aaa'])
        self.assertIsNone(obj._node)
        self.assertIsNone(obj._channel)

    def test_set_node(self):
        obj = NetDevice('myNetDevice')
        myNode = Node('myNode')
        obj.set_node(myNode)
        self.assertIsNotNone(obj._node)
        self.assertEquals('myNode', obj._node._name)

    def test_get_port_name(self):
        obj = NetDevice('myNetDevice')
        myNode = Node('myNode')
        obj.set_node(myNode)

        port_name = obj.get_port_name()

        self.assertEquals('myNetDevice', port_name)

    def test_get_tap_name(self):
        obj = NetDevice('myNetDevice')
        myNode = Node('myNode')
        obj.set_node(myNode)

        tap_name = obj.get_tap_name()

        self.assertEquals('myNode-myNetDevice.t', tap_name)

    def test_connect_to_normal(self):
        obj = NetDevice('myNetDevice')
        myNode = Node('myNode')
        obj.set_node(myNode)
        channel = Channel('myChannel')

        obj.connect_to(channel)

        self.assertEquals(True, obj.is_connected())
        self.assertIsNotNone(obj._channel)
        self.assertEquals(1, len(channel._net_devices))
        self.assertEquals('myNetDevice', channel._net_devices[0]._name)

    def test_connect_to_already_connected(self):
        obj = NetDevice('myNetDevice')
        myNode = Node('myNode')
        obj.set_node(myNode)
        channel1 = Channel('myChannel1')
        channel2 = Channel('myChannel2')

        obj.connect_to(channel1)
        obj.connect_to(channel2)

        self.assertEquals(True, obj.is_connected())
        self.assertEquals(channel1, obj._channel)
        self.assertEquals(1, len(channel1._net_devices))
        self.assertEquals('myNetDevice', channel1._net_devices[0]._name)
        self.assertEquals(0, len(channel2._net_devices))

    def test_disconnect(self):
        obj = NetDevice('myNetDevice')
        myNode = Node('myNode')
        obj.set_node(myNode)
        channel = Channel('myChannel')

        obj.connect_to(channel)
        self.assertEquals(True, obj.is_connected())

        obj.disconnect()
        self.assertEquals(False, obj.is_connected())
        self.assertIsNone(obj._channel)
        self.assertEquals(0, len(channel._net_devices))

    def test_disconnect_is_not_connected(self):
        obj = NetDevice('myNetDevice')
        myNode = Node('myNode')
        obj.set_node(myNode)
        
        self.assertEquals(False, obj.is_connected())

        obj.disconnect()
        self.assertEquals(False, obj.is_connected())


class TestNode(unittest.TestCase):
    def test___init__(self):
        obj = Node('myNode', {'key1': 'value1', 'key2': 'value2'})

        self.assertEquals('myNode', obj._name)
        self.assertEquals(2, len(obj._opts))
        self.assertEquals('value1', obj._opts['key1'])
        self.assertEquals('value2', obj._opts['key2'])
        self.assertEquals(0, len(obj._net_devices))
        self.assertEquals(False, obj._is_created)
        self.assertEquals(0, len(obj._applications))

    def test_install_net_device(self):
        obj = Node('myNode')
        myNetDevice = NetDevice('myNetDevice')

        obj.install_net_device(myNetDevice)

        self.assertEquals(True, obj._net_devices.has_key('myNetDevice'))
        self.assertEquals(myNetDevice, obj._net_devices['myNetDevice'])
        self.assertEquals('myNode', myNetDevice._node._name)

    def test_install_net_device_already_installed(self):
        obj = Node('myNode')
        myNetDevice1 = NetDevice('myNetDevice')
        myNetDevice2 = NetDevice('myNetDevice')

        obj.install_net_device(myNetDevice1)
        obj.install_net_device(myNetDevice2)

        self.assertEquals(True, obj._net_devices.has_key('myNetDevice'))
        self.assertEquals(myNetDevice1, obj._net_devices['myNetDevice'])
        self.assertEquals('myNode', myNetDevice1._node._name)
        self.assertEquals(None, myNetDevice2._node)

    def test_uninstall_net_device(self):
        obj = Node('myNode')
        myNetDevice = NetDevice('myNetDevice')

        obj.install_net_device(myNetDevice)

        obj.uninstall_net_device(myNetDevice)

        self.assertEquals(False, obj._net_devices.has_key('myNetDevice'))
        self.assertEquals(None, myNetDevice._node)

    def test_install_application(self):
        obj = Node('myNode')

        opts = {'key1': 'value1', 'key2': 'value2'}
        appimpl = DummyApplicationImpl()
        context = {'cntxtKey': 'cntxtValue'}
        application = Application('myApp', appimpl, opts, context)

        obj.install_application(application)

        self.assertEquals(1, len(obj._applications))
        self.assertEquals('myApp', obj._applications[0]._name)
        self.assertEquals('myNode', obj._applications[0]._node._name)

    def test_install_application(self):
        obj = Node('myNode')

        opts = {'key1': 'value1', 'key2': 'value2'}
        appimpl = DummyApplicationImpl()
        context = {'cntxtKey': 'cntxtValue'}
        application = Application('myApp', appimpl, opts, context)
        obj.install_application(application)

        obj.uninstall_application(application)

        self.assertEquals(0, len(obj._applications))
        self.assertEquals(None, application._node)

    def test_create(self):
        cmdlist = []
        cmdexecutor = create_cmdexecutor(cmdlist)
        obj = Node('myNode')
        obj.set_cmdexecutor(cmdexecutor)
        myChannel = Channel('myChannel')
        myNetDevice1 = NetDevice('myNetDevice1')
        myNetDevice2 = NetDevice('myNetDevice2')
        myApp1 = Application('myApp1', DummyApplicationImpl(), {}, {})
        myApp2 = Application('myApp2', DummyApplicationImpl(), {}, {})
       
        myNetDevice1.connect_to(myChannel)
        myNetDevice2.connect_to(myChannel)

        obj.install_net_device(myNetDevice1)
        obj.install_net_device(myNetDevice2)
        obj.install_application(myApp1)
        obj.install_application(myApp2)

        myNetDevice1.set_cmdexecutor(cmdexecutor)
        myNetDevice2.set_cmdexecutor(cmdexecutor)

        obj.create()

        expected_cmdlist = [
            'ip netns add myNode',
            'ip link add myNetDevice1 type veth peer name myNode-myNetDevice1.t',
            'ip link set myNetDevice1 netns myNode',
            'brctl addif myChannel myNode-myNetDevice1.t',
            'ip link set dev myNode-myNetDevice1.t up',
            'ip link add myNetDevice2 type veth peer name myNode-myNetDevice2.t',
            'ip link set myNetDevice2 netns myNode',
            'brctl addif myChannel myNode-myNetDevice2.t',
            'ip link set dev myNode-myNetDevice2.t up',
            ]
        self.assertEquals(len(expected_cmdlist), len(cmdlist))
        for idx in range(len(expected_cmdlist)):
            self.assertEquals(expected_cmdlist[idx], cmdlist[idx])
        self.assertEquals(obj, myApp1._impl._start_called_node)
        self.assertEquals(obj, myApp2._impl._start_called_node)
        self.assertEquals(True, obj._is_created)

    def test_delete(self):
        cmdlist = []
        cmdexecutor = create_cmdexecutor(cmdlist)
        obj = Node('myNode')
        myChannel = Channel('myChannel')
        myNetDevice1 = NetDevice('myNetDevice1')
        myNetDevice2 = NetDevice('myNetDevice2')
        myApp1 = Application('myApp1', DummyApplicationImpl(), {}, {})
        myApp2 = Application('myApp2', DummyApplicationImpl(), {}, {})
       
        myNetDevice1.connect_to(myChannel)
        myNetDevice2.connect_to(myChannel)

        obj.install_net_device(myNetDevice1)
        obj.install_net_device(myNetDevice2)
        obj.install_application(myApp1)
        obj.install_application(myApp2)

        obj.create()

        obj.set_cmdexecutor(cmdexecutor)
        myNetDevice1.set_cmdexecutor(cmdexecutor)
        myNetDevice2.set_cmdexecutor(cmdexecutor)

        obj.delete()

        expected_cmdlist = [
            'ip link set dev myNode-myNetDevice1.t down',
            'brctl delif myChannel myNode-myNetDevice1.t',
            'ip link delete myNode-myNetDevice1.t',
            'ip link set dev myNode-myNetDevice2.t down',
            'brctl delif myChannel myNode-myNetDevice2.t',
            'ip link delete myNode-myNetDevice2.t',
            'ip netns delete myNode',
            ]
        self.assertEquals(len(expected_cmdlist), len(cmdlist))
        for idx in range(len(expected_cmdlist)):
            self.assertEquals(expected_cmdlist[idx], cmdlist[idx])
        self.assertEquals(obj, myApp1._impl._stop_called_node)
        self.assertEquals(obj, myApp2._impl._stop_called_node)
        self.assertEquals(False, obj._is_created)

    def test_create_without_channel(self):
        cmdlist = []
        cmdexecutor = create_cmdexecutor(cmdlist)
        obj = Node('myNode')
        obj.set_cmdexecutor(cmdexecutor)
        myNetDevice1 = NetDevice('myNetDevice1')
        myNetDevice2 = NetDevice('myNetDevice2')
        myApp1 = Application('myApp1', DummyApplicationImpl(), {}, {})
        myApp2 = Application('myApp2', DummyApplicationImpl(), {}, {})

        obj.install_net_device(myNetDevice1)
        obj.install_net_device(myNetDevice2)
        obj.install_application(myApp1)
        obj.install_application(myApp2)

        myNetDevice1.set_cmdexecutor(cmdexecutor)
        myNetDevice2.set_cmdexecutor(cmdexecutor)

        obj.create()

        expected_cmdlist = [
            'ip netns add myNode',
            'ip link add myNetDevice1 type veth peer name myNode-myNetDevice1.t',
            'ip link set myNetDevice1 netns myNode',
            'ip link add myNetDevice2 type veth peer name myNode-myNetDevice2.t',
            'ip link set myNetDevice2 netns myNode',
            ]
        self.assertEquals(len(expected_cmdlist), len(cmdlist))
        for idx in range(len(expected_cmdlist)):
            self.assertEquals(expected_cmdlist[idx], cmdlist[idx])
        self.assertEquals(obj, myApp1._impl._start_called_node)
        self.assertEquals(obj, myApp2._impl._start_called_node)
        self.assertEquals(True, obj._is_created)

    def test_delete_without_channel(self):
        cmdlist = []
        cmdexecutor = create_cmdexecutor(cmdlist)
        obj = Node('myNode')
        myNetDevice1 = NetDevice('myNetDevice1')
        myNetDevice2 = NetDevice('myNetDevice2')
        myApp1 = Application('myApp1', DummyApplicationImpl(), {}, {})
        myApp2 = Application('myApp2', DummyApplicationImpl(), {}, {})

        obj.install_net_device(myNetDevice1)
        obj.install_net_device(myNetDevice2)
        obj.install_application(myApp1)
        obj.install_application(myApp2)

        obj.create()

        obj.set_cmdexecutor(cmdexecutor)
        myNetDevice1.set_cmdexecutor(cmdexecutor)
        myNetDevice2.set_cmdexecutor(cmdexecutor)

        obj.delete()

        expected_cmdlist = [
            'ip link delete myNode-myNetDevice1.t',
            'ip link delete myNode-myNetDevice2.t',
            'ip netns delete myNode',
            ]
        self.assertEquals(len(expected_cmdlist), len(cmdlist))
        for idx in range(len(expected_cmdlist)):
            self.assertEquals(expected_cmdlist[idx], cmdlist[idx])
        self.assertEquals(obj, myApp1._impl._stop_called_node)
        self.assertEquals(obj, myApp2._impl._stop_called_node)
        self.assertEquals(False, obj._is_created)


