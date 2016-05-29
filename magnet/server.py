#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib
import json
import os
import uuid

import tornado.ioloop
import tornado.web


class TopologyRequestHandler(tornado.web.RequestHandler):
    def initialize(self, api):
        self._api = api

    def get(self):
        if self._api != None:
            req_obj = self._create_jsonrpc('get-topology')
            res = self._api.operate_topology(req_obj)
            self._write_response(res)
        else:
            msg = 'get-topology not implemented yet.'
            self.set_status(httplib.NOT_IMPLEMENTED, msg)
            self.write(msg)

    def put(self):
        if self._api != None:
            topo = json.loads(self.request.body)
            req_obj = self._create_jsonrpc('create-topology', {'topology': topo})
            res = self._api.operate_topology(req_obj)
            self._write_response(res)
        else:
            msg = 'create-topology not implemented yet.'
            self.set_status(httplib.NOT_IMPLEMENTED, msg)
            self.write(msg)

    def delete(self):
        if self._api != None:
            req_obj = self._create_jsonrpc('delete-topology')
            res = self._api.operate_topology(req_obj)
            self._write_response(res)
        else:
            msg = 'delete-topology not implemented yet.'
            self.set_status(httplib.NOT_IMPLEMENTED, msg)
            self.write(msg)

    def _create_jsonrpc(self, method, params={}):
        return {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": uuid.uuid4(),
            }

    def _write_response(self, response):
        value = response.get_value()
        res_obj = None
        if value.error != None:
            res_obj = value.result
        else:
            res_obj = value
        self.write(res_obj)

def start_server(port=8888, address="", api=None):
    handlers = [
        (r"/api/v1/topology", TopologyRequestHandler, dict(api=api)),
        ]
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        }
    application = tornado.web.Application(handlers, **settings)
    application.listen(port, address)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    start_server()


