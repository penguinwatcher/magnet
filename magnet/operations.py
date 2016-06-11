#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ErrorObj:
    def __init__(self, code, message):
        self.code = code
        self.message = message


EOBJ_PARSE_ERROR = ErrorObj(-32700, 'parse error.')
EOBJ_INVALID_REQUEST = ErrorObj(-32600, 'invalid request.')
EOBJ_METHOD_NOT_FOUND = ErrorObj(-32601, 'method not found.')
EOBJ_INVALID_PARAMS = ErrorObj(-32602, 'invalid params.')
EOBJ_INTERNAL_ERROR = ErrorObj(-32603, 'internal error.')


def create_res_obj(data, req_id, error_code=None, error_message=None):
    res_obj = {}
    res_obj['jsonrpc'] = '2.0'
    res_obj['id'] = req_id
    if error_code is None:
        res_obj['result'] = data
    else:
        res_obj['error'] = {
            'code': error_code,
            'message': error_message,
            'data': data,
        }
    return res_obj


def operate_none(topology, req_obj):
    return create_res_obj(
            None,
            req_obj['id'],
            EOBJ_INTERNAL_ERROR.code,
            'not implemented yet.')


def get_operation_dict():
    return {
        'get-topology': get_topology,
        'create-topology': create_topology,
        'delete-topology': delete_topology,
    }


def get_topology(topology, req_obj):
    data = topology.to_obj()
    res_obj = create_res_obj(data, req_obj['id'])
    return res_obj


def create_topology(topology, req_obj):
    if topology.is_created():
        topology.delete()
    res_obj = None
    if 'params' in req_obj and 'topology' in req_obj['params']:
        topology_obj = req_obj['params']['topology']
        topology.setup_topology_obj(topology_obj)
        topology.create()
        data = topology.to_obj()
        res_obj = create_res_obj(data, req_obj['id'])
    else:
        res_obj = create_res_obj(
                None,
                req_obj['id'],
                EOBJ_INVALID_REQUEST.code,
                EOBJ_INVALID_REQUEST.message)
    return res_obj


def delete_topology(topology, req_obj):
    if topology.is_created():
        topology.delete()
        topology.setup_topology_obj({})
    data = topology.to_obj()
    res_obj = create_res_obj(data, req_obj['id'])
    return res_obj


# EOF
