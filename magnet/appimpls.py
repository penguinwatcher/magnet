#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from application import ApplicationImplementationBase
from cmdexecutor import exec_linux_cmd


def exec_node_cmd(cmdexecutor, node, cmd):
    cmdexecutor('ip netns exec %s %s' % (node.get_name(), cmd))


def write_lines(lines, filepath, cmdexecutor):
    if cmdexecutor is exec_linux_cmd:
        with open(filepath, 'w') as f:
            f.writelines([("%s\n" % line) for line in lines])
    else:
        if len(lines) > 0:
            first_line = lines[0]
            cmdexecutor('echo "%s" > %s' % (first_line, filepath))
        if len(lines) > 1:
            for line in lines[1:]:
                cmdexecutor('echo "%s" >> %s' % (line, filepath))


class SimpleCommand (ApplicationImplementationBase):
    def __init__(self):
        self._name = 'simple_command'

    def start(self, node, opts):
        if 'start_cmd' in opts:
            cmd = opts['start_cmd']
            exec_node_cmd(self._execc, node, cmd)

    def stop(self, node, opts):
        if 'stop_cmd' in opts:
            cmd = opts['stop_cmd']
            exec_node_cmd(self._execc, node, cmd)


class IpHelper (ApplicationImplementationBase):
    def __init__(self):
        self._name = 'ip_helper'
        self._context = None

    def application_installed(self, node, opts, context):
        self._context = context
        hostname = node.get_name()
        ipaddr = opts['ip_addr'].split('/')[0]
        if 'hosts' not in context:
            context['hosts'] = []
        host = {'hostname': hostname, 'ip_addr': ipaddr}
        context['hosts'].append(host)

    def start(self, node, opts):
        net_dev_name = opts['net_device_name']
        ipaddr = opts['ip_addr']
        if 'default_gw' in opts:
            default_gw = opts['default_gw']
        else:
            default_gw = None
        self.create_hosts_file(node, opts)
        exec_node_cmd(self._execc, node, 'ip link set lo up')
        exec_node_cmd(
                self._execc,
                node,
                ('ip addr add %s dev %s' % (ipaddr, net_dev_name)))
        exec_node_cmd(
                self._execc,
                node,
                ('ip link set %s up' % net_dev_name))
        if (default_gw is not None):
            exec_node_cmd(
                    self._execc,
                    node,
                    ('route add default gw %s' % default_gw))

    def stop(self, node, opts):
        net_dev_name = opts['net_device_name']
        exec_node_cmd(
                self._execc,
                node,
                ('ip link set %s down' % net_dev_name))
        exec_node_cmd(self._execc, node, 'ip link set lo down')
        self.delete_config_dir(node, opts)

    def create_hosts_file(self, node, opts):
        dirpath = ('/etc/netns/%s' % node.get_name())
        filepath = os.path.join(dirpath, 'hosts')
        if not os.path.exists(dirpath):
            self._execc('mkdir -p %s' % dirpath)
        self._execc('chmod -R 777 %s' % dirpath)
        if os.path.exists(filepath):
            self._execc('rm -f %s' % filepath)
        self._execc('touch %s' % filepath)
        self._execc('chmod 777 %s' % filepath)
        lines = [
            "# auto-generated by magnet",
            "127.0.0.1    localhost",
            "",
            ]
        for host in self._context['hosts']:
            line = ("%s    %s" % (host['ip_addr'], host['hostname']))
            lines.append(line)
        write_lines(lines, filepath, self._execc)

    def delete_config_dir(self, node, opts):
        dirpath = ('/etc/netns/%s' % node.get_name())
        if os.path.exists(dirpath):
            self._execc('rm -fr %s' % dirpath)


def set_default_apps(app_factory):
    def set_app(name, impl_factory):
        app_factory.register_app_impl_factory(name, impl_factory)
    set_app('ip_helper', IpHelper)
    set_app('simple_command', SimpleCommand)


if __name__ == '__main__':
    pass

# EOF
