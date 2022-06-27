#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import logging
from hashlib import md5
from flask import request, jsonify, Blueprint, redirect, url_for
from flask_security import login_required
from flask_login import current_user

from .settings import LIMIT_HASH, FLAG
from .image_model import get_image_manager
from .exifAnalyzer import exifAnalyzer

logger = logging.getLogger(__name__)

endpoints = Blueprint('endpoints', __name__, template_folder='templates')

#utils

def api_return(succes, msg):
    if not succes:
        return jsonify(status='danger', message=msg)
    return jsonify(status='success', message=msg)

def validateFileType(f):
        return '.' in f.filename\
                and (f.filename.split('.')[-1] == 'jpg' or f.filename.split('.')[-1] == 'jpg')\
                and f.content_type == "image/jpeg" and f.mimetype == "image/jpeg"

#Endpoints

@endpoints.route('/api/<string:action>', methods=['POST'])
@login_required
def api(action):
    r, msg = (False, 'Bad action')
    user = current_user.get_id()
    imageBase = get_image_manager()
    analyzer = exifAnalyzer()
    if action == 'upload':
        if len(request.files) == 1:
            f = request.files['file']
            if validateFileType(f):
                blob = f.read(LIMIT_HASH)
                f.seek(0,0)
                exif = analyzer.extract(f)
                if exif is None:
                    return api_return(False, "Max size is 500x500")
                h = md5(blob).hexdigest()
                new_filename = "%s.jpg" % (h)
                if imageBase.existByUser(new_filename, user):

                    imageBase.delImage(new_filename, user)
                    e = imageBase.addImage(new_filename, blob, user, exif, FLAG)
                    r, msg = (True, 'Successfully altered')
                    logger.info("upload;success;%s;%s" % (new_filename, exif['id']))
                else:
                    r, msg = (True, 'Successfully imported')
                    exif = analyzer.extract(f)
                    e = imageBase.addImage(new_filename, blob, user, exif, FLAG)
                    if e is not None:
                        msg = "Image imported but : %s" % e
                    logger.info("upload;success;%s;%s" % (new_filename, exif['id']))
            else:
                r, msg = (False, "Only *.jpg files can be accepted !")
                logger.info("upload;forbidden;%s;" % (f.filename))
        else:
            r,msg = (False, "Did you import a file ?")
            logger.info("upload;empty;;")
    return api_return(r, msg)

@endpoints.route('/api/del', methods=['GET'])
@login_required
def delete():
    r, msg = (False, "This file doesn't exist.")
    user = current_user.get_id()
    imageBase = get_image_manager()
    filename = request.values.get('filename', '')
    if filename is not '':
        if imageBase.existByUser(filename, user):
            if imageBase.delImage(filename, user):
                r, msg = (True, 'Successfully removed')
                logger.info("del;success;%s;%s" % (user, filename))
            else:
                r, msg = (True, 'Error')
                logger.info("del;error;%s;%s" % (user, filename))
        else:
            r, msg = (True, 'You are not allowed')
            logger.info("del;forbidden;%s;%s" % (user, filename))
    else:
        logger.info("del;failure;%s;%s" % (user, filename))
    return api_return(r, msg)
