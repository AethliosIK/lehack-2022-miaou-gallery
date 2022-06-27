#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import redis

SECRET_KEY_FLASK = os.getenv("SECRET_KEY_FLASK")
PASSWORD_SALT_FLASK = os.getenv("PASSWORD_SALT_FLASK")
LIMIT_HASH = int(os.getenv("LIMIT_HASH", "65536"))
FLAG = os.getenv("FLAG", "lh2022_{MyC41Is5OcuT3d0n'1UThINk?}")
DATABASE_URI = os.getenv("DATABASE_URI")
REDIS_URI = os.getenv("REDIS_URI")

flask_default = {
    'SECRET_KEY': SECRET_KEY_FLASK,
    'SECURITY_PASSWORD_SALT': PASSWORD_SALT_FLASK,
    'SECURITY_SEND_REGISTER_EMAIL': False,
    'SECURITY_LOGIN_USER_TEMPLATE': 'login.html',
    'SECURITY_REGISTERABLE': True,
    'SECURITY_REGISTER_USER_TEMPLATE': 'register_user.html',
    'SECURITY_CHANGE_URL': '/settings',
    'SECURITY_CHANGE_PASSWORD_TEMPLATE': 'settings.html',
    'SECURITY_CHANGEABLE': True,
    'SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL': False,
    'SECURITY_SEND_PASSWORD_CHANGE_EMAIL': False,
    'SECURITY_SEND_PASSWORD_RESET_EMAIL': False,
    'SECURITY_SEND_REGISTER_EMAIL': False,
    'SQLALCHEMY_DATABASE_URI': DATABASE_URI,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SESSION_TYPE': 'redis',
    'SESSION_PERMANENT': False,
    'SESSION_USE_SIGNER': True,
    'SESSION_REDIS': redis.from_url(REDIS_URI)
}

def init_settings(config):
    config.update(flask_default)
