#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import threading

from api import Servant, Scheduler, Proxy
from extloader import load_exts, set_ext_dict_to_topology
from server import create_server_instance
from topology import Topology


# def configure_llcli(api):
#    llcli = LowLevelCli()
#    llcli.set_api(api)
#    llcli_parser = llcli.create_argparser()
#
#    def llcli_invoke_func(argv=sys.argv[1:]):
#        args = llcli_parser.parse_args(argv)
#        args.func(args)
#
#    set_llcli_invoke_func(llcli_invoke_func)


def create_api_service(args=[]):
    # loads extensions
    ext_dict = load_exts()

    # creates api service
    servant = Servant()
    scheduler = Scheduler()
    proxy = Proxy(scheduler, servant)

    # creates topology
    topology = Topology()

    # sets extensions to topology
    set_ext_dict_to_topology(ext_dict, topology)

    return proxy


def boot(argvs):
    api_service = create_api_service()

    server_instance = create_server_instance(port=8888, api=api_service)

    def api_service_task():
        try:
            logging.info('Starting api service.')
            api_service.start()
        finally:
            logging.info('api service stopped.')

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

    th_api_service = start_thread_as_daemon(
            target=api_service_task,
            name='api_service_thread')
    th_server_instance = start_thread_as_daemon(
            target=server_instance_task,
            name='server_instance_thread')

    th_api_service.join()
    th_server_instance.join()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    argvs = sys.argv
    boot(argvs)

# EOF
