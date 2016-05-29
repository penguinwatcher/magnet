#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

if __name__ == '__main__':
    sys.path.append('./magnet')
    sys.path.append('./test')
    setup(
        name = 'magnet',
        packages = find_packages(),
        entry_points = """
        [console_scripts]
        magnet-llcli=magnet.llcli:invoke_llcli
        """
    )

