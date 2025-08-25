#!/usr/bin/env python

"""
    Configurations for Public Readium Service

    :copyright: (c) 2015 by AUTHORS
    :license: see LICENSE for more details
"""

import os
import netifaces

def get_default_gateway_ip():
    if _gateways := netifaces.gateways():
        if 'default' in _gateways:
            return _gateways['default'][netifaces.AF_INET][0]

# Determine environment
TESTING = os.getenv("TESTING", "false").lower() == "true"

# API server configuration
HOST = os.environ.get('PRS_HOST', '0.0.0.0')
PORT = int(os.environ.get('PRS_PORT', 8080))
BASE_URL = os.environ.get('PRS_BASE_URL', '')
READIUM_HOST_PORT = os.environ.get('NOMAD_ADDR_readium', 'prs_readium:15080')
READER_HOST_PORT = os.environ.get('NOMAD_ADDR_reader', 'prs_reader:3000')

WORKERS = int(os.environ.get('PRS_WORKERS', 1))
DEBUG = bool(int(os.environ.get('PRS_DEBUG', 0)))
GATEWAY = get_default_gateway_ip()
LOG_LEVEL = os.environ.get('PRS_LOG_LEVEL', 'info')

OPTIONS = {
    'host': HOST,
    'port': PORT,
    'log_level': LOG_LEVEL,
    'reload': DEBUG,
    'workers': WORKERS,
}

__all__ = ['BASE_URL', 'HOST', 'PORT', 'DEBUG', 'OPTIONS', 'TESTING']
