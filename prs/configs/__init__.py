#!/usr/bin/env python

"""
    Configurations for Public Readium Service

    :copyright: (c) 2015 by AUTHORS
    :license: see LICENSE for more details
"""

import os

# Determine environment
TESTING = os.getenv("TESTING", "false").lower() == "true"

# API server configuration
DOMAIN = os.environ.get('PRS_DOMAIN', '127.0.0.1')
HOST = os.environ.get('PRS_HOST', '0.0.0.0')
PORT = int(os.environ.get('PRS_PORT', 8080))
WORKERS = int(os.environ.get('PRS_WORKERS', 1))
DEBUG = bool(int(os.environ.get('PRS_DEBUG', 0)))

LOG_LEVEL = os.environ.get('PRS_LOG_LEVEL', 'info')
SSL_CRT = os.environ.get('PRS_SSL_CRT')
SSL_KEY = os.environ.get('PRS_SSL_KEY')

OPTIONS = {
    'host': HOST,
    'port': PORT,
    'log_level': LOG_LEVEL,
    'reload': DEBUG,
    'workers': WORKERS,
}
if SSL_CRT and SSL_KEY:
    OPTIONS['ssl_keyfile'] = SSL_KEY
    OPTIONS['ssl_certfile'] = SSL_CRT

__all__ = ['DOMAIN', 'HOST', 'PORT', 'DEBUG', 'OPTIONS', 'TESTING']
