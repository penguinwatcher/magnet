#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib
import json
import os
import uuid
import logging

import tornado.ioloop
import tornado.web


class TopologyRequestHandler(tornado.web.RequestHandler):
    def initialize(self, api):
        self._api = api

    def get(self):
        if self._api is not None:
            req_obj = self._create_req_obj('get-topology')
            res = self._api.operate_topology(req_obj)
            self._write_response(res)
        else:
            msg = 'get-topology not implemented yet.'
            self.set_status(httplib.NOT_IMPLEMENTED, msg)
            self.write(msg)

    def put(self):
        if self._api is not None:
            topo = json.loads(self.request.body)
            req_obj = self._create_req_obj(
                    'create-topology',
                    {'topology': topo})
            res = self._api.operate_topology(req_obj)
            self._write_response(res)
        else:
            msg = 'create-topology not implemented yet.'
            self.set_status(httplib.NOT_IMPLEMENTED, msg)
            self.write(msg)

    def delete(self):
        if self._api is not None:
            req_obj = self._create_req_obj('delete-topology')
            res = self._api.operate_topology(req_obj)
            self._write_response(res)
        else:
            msg = 'delete-topology not implemented yet.'
            self.set_status(httplib.NOT_IMPLEMENTED, msg)
            self.write(msg)

    def _create_req_obj(self, method, params={}):
        return {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": str(uuid.uuid4()),
            }

    def _write_response(self, response):
        value = response.get_value()
        import json
        print json.dumps(value)
        res_obj = None
        if 'error' not in value or value['error'] is None:
            res_obj = value['result']
        else:
            res_obj = value
        self.write(json.dumps(res_obj))


def create_server_instance(port=8888, address="", api=None):
    handlers = [
        (r"/api/v1/topology", TopologyRequestHandler, dict(api=api)),
        ]
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        }
    logging.info('Starting server %s:%d' % (address, port))
    application = tornado.web.Application(handlers, **settings)
    application.listen(port, address)
    return tornado.ioloop.IOLoop.instance()


def start_server(port=8888, address="", api=None):
    server_instance = create_server_instance(port, address, api)
    server_instance.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    start_server()

# EOF
