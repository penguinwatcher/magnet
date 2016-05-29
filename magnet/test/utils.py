#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


def create_cmdexecutor(cmdlist):
    def func(cmd):
        logging.debug('Executing ... %s' % cmd)
        cmdlist.append(cmd)
        return 0
    return func

# EOF
