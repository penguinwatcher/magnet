#!/usr/bin/env python
# -*- coding: utf-8 -*-

from magnet.application import ApplicationImplementationBase

class DummyApplicationImpl(ApplicationImplementationBase):
    def __init__(self):
        self._start_called_node = None
        self._start_called_opts = None
        self._stop_called_node = None
        self._stop_called_opts = None
        self._application_installed_called_node = None
        self._application_installed_called_opts = None
        self._application_installed_called_context = None

    def start(self, node, opts):
        self._start_called_node = node
        self._start_called_opts = opts

    def stop(self, node, opts):
        self._stop_called_node = node
        self._stop_called_opts = opts

    def application_installed(self, node, opts, context):
        self._application_installed_called_node = node
        self._application_installed_called_opts = opts
        self._application_installed_called_context = context


