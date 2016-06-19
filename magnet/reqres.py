#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid


def create_req_obj(method, params={}):
    return {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": str(uuid.uuid4()),
        }


def create_get_topology_req_obj():
    return create_req_obj('get-topology')


def create_create_topology_req_obj(topo_obj):
    return create_req_obj('create-topology', {'topology': topo_obj})


def create_delete_topology_req_obj():
    return create_req_obj('delete-topology')

# EOF
