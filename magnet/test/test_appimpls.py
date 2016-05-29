#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import unittest

from magnet.appimpls import exec_node_cmd
from magnet.appimpls import IpHelper 
from magnet.appimpls import SimpleCommand 
from magnet.components import Node 
from magnet.test.utils import create_cmdexecutor


class TestExecNodeCmd(unittest.TestCase):
    def test_exec_node_cmd(self):
        cmdlist = []
        cmdexecutor = create_cmdexecutor(cmdlist)
        node = Node('myNode')
        cmd = 'do something'

        exec_node_cmd(cmdexecutor, node, cmd)

        self.assertEquals(1, len(cmdlist))
        self.assertEquals('ip netns exec myNode do something', cmdlist[0])


class TestSimpleCommand(unittest.TestCase):
    def test___init__(self):
        obj = SimpleCommand()
        self.assertEquals('simple_command', obj._name)

    def test_start(self):
        cmdlist = []
        obj = SimpleCommand()
        obj.set_cmdexecutor(create_cmdexecutor(cmdlist))
        node = Node('myNode')
        opts = {
            'start_cmd': 'do my start command',
            'stop_cmd': 'do my stop command',
            }

        obj.start(node, opts)

        self.assertEquals(1, len(cmdlist))
        self.assertEquals('ip netns exec myNode do my start command', cmdlist[0])

    def test_stop(self):
        cmdlist = []
        obj = SimpleCommand()
        obj.set_cmdexecutor(create_cmdexecutor(cmdlist))
        node = Node('myNode')
        opts = {
            'start_cmd': 'do my start command',
            'stop_cmd': 'do my stop command',
            }

        obj.stop(node, opts)

        self.assertEquals(1, len(cmdlist))
        self.assertEquals('ip netns exec myNode do my stop command', cmdlist[0])

    def test_start_without_start_cmd(self):
        cmdlist = []
        obj = SimpleCommand()
        obj.set_cmdexecutor(create_cmdexecutor(cmdlist))
        node = Node('myNode')
        opts = {}

        obj.start(node, opts)

        self.assertEquals(0, len(cmdlist))

    def test_stop_without_stop_cmd(self):
        cmdlist = []
        obj = SimpleCommand()
        obj.set_cmdexecutor(create_cmdexecutor(cmdlist))
        node = Node('myNode')
        opts = {}

        obj.stop(node, opts)

        self.assertEquals(0, len(cmdlist))


class TestIpHelper(unittest.TestCase):
    def test___init__(self):
        obj = IpHelper()

        self.assertEquals('ip_helper', obj._name)
        self.assertIsNone(obj._context)

