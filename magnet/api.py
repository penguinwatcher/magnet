#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
import threading
import json

from topology import Topology

class Api:
    def operate_topology(self, cmd_obj): abstract

class Service:
    def start(self): abstract
    def stop(self): abstract

class Servant(Api):
    def __init__(self, topology=None):
        self._topology = topology

    def operate_topology(self, jsonrpc_req_obj):
        print json.dumps(jsonrpc_req_obj)
        # operates topology here.
        jsonrpc_res_obj = {
                "jsonrpc": "2.0",
                "result": null,
                "error": {
                        "code": -32603,
                        "message": "not implemented yet",
                        "data": null
                    },
                "id": cmd_obj["id"]
            }
        return RealResponse(jsonrpc_res_obj)

class Response:
    def get_value(self): abstract

class FutureResponse(Response):
    def __init__(self):
        self._cond = threading.Condition()
        self._is_ready = False
        self._response = None

    def set_response(self, response):
        with self._cond:
            self._response = response
            self._is_ready = True
            self._cond.notify_all()

    def get_value(self):
        with self._cond:
            while not self._is_ready:
                self._cond.wait()
            return self._response.get_value()

class RealResponse(Response):
    def __init__(self, value):
        self._value = value

    def get_value(self):
        return self._value

class Request:
    def __init__(self, servant, future):
        self._servant = servant
        self._future = future

    def execute(self): abstract

class OperateTopologyRequest(Request):
    def __init__(self, servant, future, cmd_obj):
        Request.__init__(self, servant, future)
        self._cmd_obj = cmd_obj

    def execute(self):
        res = self._servant.operate_topology(self._cmd_obj)
        self._future.set_response(res)


class Scheduler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name="scheduler-thread")
        self._queue = Queue.Queue()
        self._is_stopped = False
    
    def invoke(self, request):
        self._queue.put(request)

    def run(self):
        while not self._is_stopped:
            request = self._queue.get()
            request.execute()

    def stop(self):
        self._is_stopped = True

class Proxy(Api, Service):
    def __init__(self, scheduler, servant):
        self._scheduler = scheduler
        self._servant = servant

    def start(self):
        self._scheduler.start()

    def stop(self):
        self._scheduler.stop()

    def operate_topology(self, cmd_obj):
        future = FutureResponse()
        req = OperateTopologyRequest(self._servant, future, cmd_obj)
        self._scheduler.invoke(req)
        return future

def create_api_service():
    servant = Servant()
    scheduler = Scheduler()
    proxy = Proxy(scheduler, servant)
    return proxy

if __name__ == '__main__':
    import time
    import random

    api_service = create_api_service()

    class ClientA(threading.Thread):
        def run(self):
            for idx in range(1, 10):
                time.sleep(random.randint(1, 4))
                future = api_service.operate_topology("cmd-a-%d" % idx)
                print future.get_value()

    class ClientB(threading.Thread):
        def run(self):
            for idx in range(1, 10):
                time.sleep(random.randint(1, 6))
                future = api_service.operate_topology("cmd-b-%d" % idx)
                print future.get_value()

    client_a = ClientA()
    client_b = ClientB()

    api_service.start()
    client_a.start()
    client_b.start()
    


