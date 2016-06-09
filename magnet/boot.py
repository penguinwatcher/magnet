#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from topology import Topology
from extloader import load_exts, set_ext_dict_to_topology
from api import Servant, Scheduler, Proxy
from llcli import LowLevelCli, set_llcli_invoke_func


def boot(argvs):
    # loads extensions
    ext_dict = load_exts()

    # creates api service
    servant = Servant()
    scheduler = Scheduler()
    api_service = Proxy(scheduler, servant)

    # creates llcli
    llcli = LowLevelCli()
    llcli.set_api(api_service)
    llcli_parser = llcli.create_argparser()

    def llcli_invoke_func(argv=sys.argv[1:]):
        args = llcli_parser.parse_args(argv)
        args.func(args)

    set_llcli_invoke_func(llcli_invoke_func)

    # creates topology
    topology = Topology()

    # sets extensions to topology
    set_ext_dict_to_topology(ext_dict, topology)

    # starts api service
    api_service.start()


if __name__ == '__main__':
    argvs = sys.argv
    boot(argvs)

# EOF
