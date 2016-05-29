#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from cmdexecutor import exec_nothing


class ApplicationImplementationBase:
    def set_cmdexecutor(self, cmdexecutor):
        self._execc = cmdexecutor

    def application_installed(self, node, opts, context):
        pass

    def start(self, node, opts):
        pass

    def stop(self, node, opts):
        pass


class NullApplicationImplementation (ApplicationImplementationBase):
    def application_installed(self, node, opts, context):
        logging.info('null application - application_installed')

    def start(self, node, opts):
        logging.info('null application - start')

    def stop(self, node, opts):
        logging.info('null application - stop')


class Application:
    def __init__(self, name, impl, opts, context):
        self._name = name
        self._opts = opts
        self._impl = impl
        self._context = context
        self._node = None

    def get_name(self):
        return self._name

    def create(self):
        if self._impl is not None:
            self._impl.start(self._node, self._opts)

    def delete(self):
        if self._impl is not None:
            self._impl.stop(self._node, self._opts)

    def set_node(self, node):
        self._node = node
        if self._impl is not None:
            self._impl.application_installed(node, self._opts, self._context)


class ApplicationFactory:
    def __init__(self, cmdexecutor=exec_nothing):
        self._impl_factory_dict = {}
        self._app_context_dict = {}
        self._execc = cmdexecutor

    def set_cmdexecutor(self, cmdexecutor):
        self._execc = cmdexecutor

    def create_application(self, app_name, opts={}):
        app_context = None
        if app_name in self._impl_factory_dict:
            impl_factory = self._impl_factory_dict[app_name]
            app_context = self._app_context_dict[app_name]
        else:
            impl_factory = NullApplicationImplementation
            app_context = {}
        impl = impl_factory()
        impl.set_cmdexecutor(self._execc)
        return Application(app_name, impl, opts, app_context)

    def register_app_impl_factory(self, app_name, impl_factory):
        self._impl_factory_dict[app_name] = impl_factory
        self._app_context_dict[app_name] = {}


if __name__ == '__main__':
    pass

# EOF
