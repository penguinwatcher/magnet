#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import codecs
import httplib
import logging
import os.path
import sys


def do_json_request(host, port, path, json_req_body='', method='GET'):
    conn = httplib.HTTPConnection(host, port)
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
        host = args.host
        port = args.port
        path = '/api/v1/topology'
        res_body = do_json_request(host, port, path)
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
            required=True,
            help='topology configuration file.')

    def invoke(args):
        logging.debug('args: %s', args)
        json_filepath = args.file.pop(0)
        logging.debug('json_filepath: %s', json_filepath)
        if os.path.exists(json_filepath):
            data = None
            with codecs.open(json_filepath, 'r', 'utf-8') as jsonf:
                data = jsonf.read()
            if data is not None:
                host = args.host
                port = args.port
                path = '/api/v1/topology'
                method = 'PUT'
                res_body = do_json_request(host, port, path, data, method)
                print res_body
        else:
            sys.stderr.write('File not found.: %s\n' % json_filepath)

    subparser.set_defaults(func=invoke)


def setup_delete_topology_subparser(subparsers):
    subparser = subparsers.add_parser(
            'delete-topology',
            help='deletes topology.')

    def invoke(args):
        logging.debug('args: %s', args)
        host = args.host
        port = args.port
        path = '/api/v1/topology'
        method = 'DELETE'
        res_body = do_json_request(host, port, path, method=method)
        print res_body

    subparser.set_defaults(func=invoke)


class Cli:
    def __init__(self):
        self._typeName = 'Cli'

    def create_argparser(self):
        parser = argparse.ArgumentParser(
                description='magnet command line interface')

        parser.add_argument(
                '-v',
                '--verbose',
                default=False,
                action='store_true',
                help='verbose.')
        parser.add_argument(
                '--host',
                default='127.0.0.1',
                help='host name, e.g. example.org, 192.0.2.10 and so on.')
        parser.add_argument(
                '--port',
                default='8888',
                type=int,
                help='port number.')

        subparsers = parser.add_subparsers(help='operation commands.')

        setup_get_topology_subparser(subparsers)
        setup_create_topology_subparser(subparsers)
        setup_delete_topology_subparser(subparsers)

        return parser


def invoke_cli(args=sys.argv[1:]):
    cli = Cli()
    parser = cli.create_argparser()
    args_obj = parser.parse_args(args)
    if args_obj.verbose:
        logging.basicConfig(level=logging.DEBUG)
    args_obj.func(args_obj)


if __name__ == '__main__':
    invoke_cli()

# EOF
