#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import exifread
import PIL.Image

MAX_SIZE = 500

class exifAnalyzer:
    def __init__(self):
        pass

    def extract(self, f):
        r = {}
        with PIL.Image.open(f) as img:
            if img.size[0] > MAX_SIZE or img.size[1] > MAX_SIZE:
                return None
            tags2 = img._getexif()
            r['id'] = "0"
            if tags2 is not None and 42016 in tags2:
                r['id'] = tags2[42016]
        f.seek(0,0)
        tags = exifread.process_file(f)
        r['artist'] = None
        if "Image Artist" in tags:
            r['artist'] = tags["Image Artist"]
        r['copyright'] = None
        if "Image Copyright" in tags:
            r['copyright'] = tags["Image Copyright"]
        return r
