#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging

def init_logger(loglevel):
    try:
        loglevel = int(logging.getLevelName(loglevel))
    except ValueError:
        loglevel = logging.ERROR
    logging.basicConfig(
            level=loglevel,
            format="[%(asctime)s] [%(name)s.%(funcName)s:%(lineno)d] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S %z", stream=sys.stdout)

