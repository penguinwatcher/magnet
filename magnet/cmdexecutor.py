#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import logging


def exec_nothing(cmd):
    logging.debug('Executing ... %s' % cmd)
    return 0


def exec_linux_cmd(cmd):
    logging.debug('Executing ... %s' % cmd)
    returncode = 0
    returncode = subprocess.call(cmd.strip().split(' '))
    return returncode

# EOF
