#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

if __name__ == '__main__':
    sys.path.append('./magnet')
    sys.path.append('./test')
    setup(
        name = 'magnet',
        version = '0.1.0',
        packages = find_packages(),
        install_requires = [
            'tornado',
        ],
        entry_points = """
        [console_scripts]
        magnet=magnet.boot:boot
        magnet-llcli=magnet.llcli:invoke_llcli
        """
    )

