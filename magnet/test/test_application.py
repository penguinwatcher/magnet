#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from magnet.application import NullApplicationImplementation
from magnet.application import Application
from magnet.application import ApplicationFactory
from magnet.components import Node
from magnet.cmdexecutor import exec_nothing
from magnet.test.dummyapplicationimpl import DummyApplicationImpl

class TestApplication(unittest.TestCase):
    def test___init__(self):
        name = 'myApp'
        impl = DummyApplicationImpl()
        opts = {'key1': 'value1', 'key2': 'value2'}
        context = {'cntxtKey', 'cntxtValue'}

        obj = Application(name, impl, opts, context)

        self.assertEquals('myApp', obj._name)
        self.assertEquals(opts, obj._opts)
        self.assertEquals(impl, obj._impl)
        self.assertEquals(context, obj._context)
        self.assertEquals(None, obj._node)

    def test_set_node(self):
        impl = DummyApplicationImpl()
        opts = {'key1': 'value1', 'key2': 'value2'}
        context = {'cntxtKey', 'cntxtValue'}
        obj = Application('myApp', impl, opts, context)

        node = Node('myNode')

        obj.set_node(node)

        self.assertEquals('myNode', obj._node._name)
        self.assertEquals(node, obj._impl._application_installed_called_node)
        self.assertEquals(opts, obj._impl._application_installed_called_opts)
        self.assertEquals(context, obj._impl._application_installed_called_context)

    def test_set_node_impl_is_none(self):
        impl = None
        opts = None
        context = None
        obj = Application('myApp', impl, opts, context)

        node = Node('myNode')

        obj.set_node(node)

        self.assertEquals('myNode', obj._node._name)

    def test_create(self):
        impl = DummyApplicationImpl()
        opts = {}
        obj = Application('myApp', impl, opts, {})

        node = Node('myNode')
        obj.set_node(node)

        obj.create()

        self.assertEquals(node, obj._impl._start_called_node)
        self.assertEquals(opts, obj._impl._start_called_opts)

    def test_delete(self):
        impl = DummyApplicationImpl()
        opts = {}
        obj = Application('myApp', impl, opts, {})

        node = Node('myNode')
        obj.set_node(node)
        obj.create()

        obj.delete()

        self.assertEquals(node, obj._impl._stop_called_node)
        self.assertEquals(opts, obj._impl._stop_called_opts)

class TestApplicationFactory(unittest.TestCase):
    def test___init__(self):
        context = {'cmdexecutor': exec_nothing}
        obj = ApplicationFactory(context)

        self.assertEquals(0, len(obj._impl_factory_dict))
        self.assertEquals(0, len(obj._app_context_dict))
        self.assertIsNotNone(obj._execc)

    def test_register_app_impl_factory(self):
        obj = ApplicationFactory()

        obj.register_app_impl_factory('dummy', DummyApplicationImpl)

        self.assertEquals(1, len(obj._impl_factory_dict))
        self.assertEquals(True, obj._impl_factory_dict.has_key('dummy'))
        self.assertEquals(1, len(obj._app_context_dict))
        self.assertEquals(0, len(obj._app_context_dict['dummy']))

    def test_create_application(self):
        obj = ApplicationFactory()
        obj.register_app_impl_factory('dummy', DummyApplicationImpl)
        opts = {'key1': 'value1'}

        app = obj.create_application('dummy', opts)

        self.assertIsNotNone(app)
        self.assertTrue(isinstance(app._impl, DummyApplicationImpl))
        self.assertEquals(1, len(app._opts))
        self.assertEquals('value1', app._opts['key1'])

    def test_create_application_null_application(self):
        obj = ApplicationFactory()
        obj.register_app_impl_factory('dummy', DummyApplicationImpl)
        opts = {'key1': 'value1'}

        app = obj.create_application('hoge', opts)

        self.assertIsNotNone(app)
        self.assertTrue(isinstance(app._impl, NullApplicationImplementation))
        self.assertEquals(1, len(app._opts))
        self.assertEquals('value1', app._opts['key1'])

