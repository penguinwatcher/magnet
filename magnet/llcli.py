#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys


class LowLevelCli:
    def __init__(self):
        self._typeName = 'LowLevelCli'
        self._api = None

    def set_api(self, api):
        self._api = api

    def create_argparser(self):
        parser = argparse.ArgumentParser(
                description='magnet low level command line interface')
        subparsers = parser.add_subparsers(help='operation command.')

        def setup_create_topo_parser():
            subparser = subparsers.add_parser(
                    'create-topology',
                    help='topology creation command.')
            subparser.add_argument(
                    '-f',
                    '--file',
                    nargs=1,
                    help='topology configuration file.')
            subparser.set_defaults(func=self.invoke_create_topology)

        def setup_delete_topo_parser():
            subparser = subparsers.add_parser(
                    'delete-topology',
                    help='topology deletion command.')
            subparser.set_defaults(func=self.invoke_delete_topology)

        setup_create_topo_parser()
        setup_delete_topo_parser()
        return parser

    def invoke_create_topology(self, args):
        print args
        if self._api is not None:
            pass
        else:
            print self._typeName
            print ("creating topology with args %s ... done" % args)

    def invoke_delete_topology(self, args):
        print args
        if self._api is not None:
            pass
        else:
            print self._typeName
            print ("deleting topology with args %s ... done" % args)


def create_invoke_func():
    cli = LowLevelCli()
    # cli.set_api(get_api())
    parser = cli.create_argparser()

    def invoke(argv=sys.argv[1:]):
        args = parser.parse_args(argv)
        args.func(args)
    return invoke


invoke_llcli = None


def set_llcli_invoke_func(func):
    invoke_llcli = func


if __name__ == '__main__':
    invoke_llcli()

# EOF
