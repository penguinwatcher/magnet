#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from cmdexecutor import exec_nothing


class Channel:
    """Channel class"""
    def __init__(self, name, opts={}):
        self._name = name
        self._opts = opts
        self._execc = exec_nothing
        self._net_devices = []

    def get_name(self):
        return self._name

    def set_cmdexecutor(self, cmdexecutor):
        self._execc = cmdexecutor
        return self

    def create(self):
        """Creates this channel as a bridge w/o spanning-tree protocol."""
        self._execc('brctl addbr %s' % (self._name,))
        self._execc('brctl stp %s off' % (self._name,))
        self._execc('ip link set dev %s up' % (self._name,))

    def delete(self):
        """Deletes this channel."""
        self._execc('ip link set dev %s down' % (self._name,))
        self._execc('brctl delbr %s' % (self._name,))

    def append_net_device(self, net_device):
        self._net_devices.append(net_device)

    def remove_net_device(self, net_device):
        self._net_devices.remove(net_device)


class NetDevice:
    """Net device class."""
    def __init__(self, name, opts={}):
        self._name = name
        self._opts = opts
        self._execc = exec_nothing
        self._node = None
        self._channel = None

    def get_name(self):
        return self._name

    def set_cmdexecutor(self, cmdexecutor):
        self._execc = cmdexecutor
        return self

    def set_node(self, node):
        self._node = node

    def get_port_name(self):
        return self._name

    def get_tap_name(self):
        return '%s-%s.t' % (self._node._name, self._name)

    def create(self):
        self._execc(
            'ip link add %s type veth peer name %s'
            % (self.get_port_name(), self.get_tap_name()))
        self._execc(
            'ip link set %s netns %s'
            % (self.get_port_name(), self._node._name))
        if self.is_connected():
            tap_name = self.get_tap_name()
            self._execc(
                    'brctl addif %s %s'
                    % (self._channel._name, tap_name))
            self._execc('ip link set dev %s up' % (tap_name,))

    def delete(self):
        if self.is_connected():
            tap_name = self.get_tap_name()
            self._execc('ip link set dev %s down' % (tap_name,))
            self._execc(
                    'brctl delif %s %s'
                    % (self._channel._name, tap_name))
        self._execc('ip link delete %s' % (self.get_tap_name(),))

    def is_connected(self):
        return self._channel is not None

    def connect_to(self, channel):
        if not self.is_connected():
            self._channel = channel
            channel.append_net_device(self)

    def disconnect(self):
        if self.is_connected():
            channel = self._channel
            self._channel = None
            channel.remove_net_device(self)


class Node:
    """Node class"""
    def __init__(self, name, opts={}):
        self._name = name
        self._opts = opts
        self._execc = exec_nothing
        self._net_devices = OrderedDict()
        self._is_created = False
        self._applications = []

    def get_name(self):
        return self._name

    def set_cmdexecutor(self, cmdexecutor):
        self._execc = cmdexecutor
        return self

    def create(self):
        """Creates this node as a netns."""
        self._execc('ip netns add %s' % (self._name,))
        # Sets all net devices.
        for name, dev in self._net_devices.iteritems():
            dev.create()
        for app in self._applications:
            app.create()
        self._is_created = True

    def delete(self):
        for app in self._applications:
            app.delete()
        # Unsets all net devices.
        for name, dev in self._net_devices.iteritems():
            dev.delete()
        self._execc('ip netns delete %s' % (self._name,))
        self._is_created = False

    def install_net_device(self, net_device):
        if net_device._name not in self._net_devices:
            self._net_devices[net_device._name] = net_device
            net_device.set_node(self)

    def uninstall_net_device(self, net_device):
        if net_device._name in self._net_devices:
            del self._net_devices[net_device._name]
            net_device.set_node(None)

    def install_application(self, application):
        self._applications.append(application)
        application.set_node(self)

    def uninstall_application(self, application):
        self._applications.remove(application)
        application.set_node(None)

if __name__ == '__main__':
    pass

# EOF
