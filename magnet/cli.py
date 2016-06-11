#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import httplib
import logging
import sys


def do_json_request(
        path,
        host='127.0.0.1:8888',
        json_req_body='',
        method='GET'):
    conn = httplib.HTTPConnection(host)
    headers = {
        'Cotent-type': 'application/json',
        'Accept': 'application/json',
        }
    conn.request(method, path, json_req_body, headers)
    res = conn.getresponse()
    data = res.read()
    logging.debug('(status, reason)=(%d, %s)', res.status, res.reason)
    logging.debug('body=%s', data)
    conn.close()
    return data


def setup_get_topology_subparser(subparsers):
    subparser = subparsers.add_parser(
            'get-topology',
            help='obtains topology.')

    def invoke(args):
        logging.debug('args: %s', args)
        res_body = do_json_request('/api/v1/topology')
        print res_body

    subparser.set_defaults(func=invoke)


def setup_create_topology_subparser(subparsers):
    subparser = subparsers.add_parser(
            'create-topology',
            help='creates topology.')
    subparser.add_argument(
            '-f',
            '--file',
            nargs=1,
            help='topology configuration file.')

    def invoke(args):
        pass

    subparser.set_defaults(func=invoke)


def setup_delete_topology_subparser(subparsers):
    subparser = subparsers.add_parser(
            'delete-topology',
            help='deletes topology.')

    def invoke(args):
        pass

    subparser.set_defaults(func=invoke)


class Cli:
    def __init__(self):
        self._typeName = 'Cli'

    def create_argparser(self):
        parser = argparse.ArgumentParser(
                description='magnet command line interface')

        subparsers = parser.add_subparsers(help='operation commands.')

        setup_get_topology_subparser(subparsers)
        setup_create_topology_subparser(subparsers)
        setup_delete_topology_subparser(subparsers)

        return parser


def invoke_cli(args=sys.argv[1:]):
    cli = Cli()
    parser = cli.create_argparser()
    args_obj = parser.parse_args(args)
    args_obj.func(args_obj)


if __name__ == '__main__':
    invoke_cli()

# EOF
