#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Queue
import threading
import json

from operations import operate_none, create_res_obj, EOBJ_INTERNAL_ERROR
from reqres import create_delete_topology_req_obj


class Request:
    def __init__(self, servant, future):
        self._servant = servant
        self._future = future

    def execute(self):
        pass


class OperateTopologyRequest(Request):
    def __init__(self, servant, future, req_obj):
        Request.__init__(self, servant, future)
        self._req_obj = req_obj

    def execute(self):
        res = self._servant.operate_topology(self._req_obj)
        self._future.set_response(res)


class Response:
    def get_value(self):
        pass


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


class Api:
    def operate_topology(self, req_obj):
        pass


class Service:
    def start(self):
        pass

    def stop(self):
        pass


class Servant(Api):
    def __init__(self, topology=None):
        self._topology = topology
        self._operation_dict = {}

    def set_operation_dict(self, operation_dict):
        self._operation_dict = operation_dict

    def operate_topology(self, req_obj):
        logging.info(json.dumps(req_obj))
        # operates topology here.
        operation = self.get_operation(req_obj['method'])
        if self._topology is not None:
            res_obj = operation(self._topology, req_obj)
        else:
            res_obj = create_res_obj(
                    None,
                    req_obj['id'],
                    EOBJ_INTERNAL_ERROR.code,
                    'topology is not setup.')
        return RealResponse(res_obj)

    def get_operation(self, method_name):
        operation = None
        if method_name in self._operation_dict:
            operation = self._operation_dict[method_name]
        if operation is None:
            operation = operate_none
        return operation


class Scheduler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name="scheduler-thread")
        self._queue = Queue.Queue()
        self._is_stopped = False

    def invoke(self, request):
        self._queue.put(request)

    def run(self):
        try:
            timeout_sec = 4.0
            logging.info('starting scheduler-task.')
            while not self._is_stopped:
                try:
                    request = self._queue.get(
                            block=True,
                            timeout=timeout_sec)
                    request.execute()
                except Queue.Empty:
                    pass
        finally:
            logging.info('scheduler-task stopped.')

    def stop(self):
        self._is_stopped = True


class Proxy(Api, Service):
    def __init__(self, scheduler, servant):
        self._scheduler = scheduler
        self._servant = servant

    def start(self):
        logging.info('proxy started.')
        self._scheduler.start()

    def stop(self):
        logging.info('cleaning topology.')
        self.clean_topology()
        logging.info('topology cleaned.')
        self._scheduler.stop()
        logging.info('waiting scheduler stopped.')
        self._scheduler.join(30.0)
        logging.info('proxy stopped.')

    def operate_topology(self, req_obj):
        future = FutureResponse()
        req = OperateTopologyRequest(self._servant, future, req_obj)
        self._scheduler.invoke(req)
        return future

    def clean_topology(self):
        req_obj = create_delete_topology_req_obj()
        future = self.operate_topology(req_obj)
        future.get_value()


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

# EOF
