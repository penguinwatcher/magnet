#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import threading

from api import Servant, Scheduler, Proxy
from cmdexecutor import exec_linux_cmd
from extloader import load_exts, set_ext_dict_to_topology
from operations import get_operation_dict
from server import create_server_instance
from topology import Topology


def create_api_service(opts={}):
    # loads extensions
    ext_dict = load_exts()

    # creates topology
    topology = Topology()

    # creates api service
    servant = Servant(topology)
    scheduler = Scheduler()
    proxy = Proxy(scheduler, servant)

    # configures api service
    scheduler.daemon = True
    servant.set_operation_dict(get_operation_dict())

    # configures topology
    set_ext_dict_to_topology(ext_dict, topology)
    if 'is_exec_nothing' not in opts or not opts['is_exec_nothing']:
        topology.set_cmdexecutor(exec_linux_cmd)

    return proxy


def boot(argvs=[]):
    logging.basicConfig(level=logging.DEBUG)

    api_service = create_api_service()

    server_instance = create_server_instance(port=8888, api=api_service)

    def server_instance_task():
        try:
            logging.info('Starting server instance.')
            server_instance.start()
        finally:
            logging.info('server instance stopped.')

    def start_thread_as_daemon(target, name):
        th = threading.Thread(target=target, name=name)
        th.daemon = True
        th.start()
        return th

    api_service.start()
    
    th_server_instance = start_thread_as_daemon(
            target=server_instance_task,
            name='server_instance_thread')

    server_instance_join_timeout = 10.0
    while th_server_instance.is_alive():
        try:
            th_server_instance.join(server_instance_join_timeout)
        except KeyboardInterrupt, SystemExit:
            logging.info('Interrupted')
            server_instance.stop()
            api_service.stop()
    logging.info('main thread terminated.')


if __name__ == '__main__':
    argvs = sys.argv
    boot(argvs)

# EOF
