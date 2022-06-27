#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, url_for, send_file
from flask_security import login_required
from flask_login import current_user

from .image_model import get_image_manager

index = Blueprint('index', __name__)

@index.route('/')
def index_f():
    return render_template('home.html', name="Welcome")

@index.route('/gallery')
@login_required
def gallery():
    imageBase = get_image_manager()
    user = current_user.get_id()
    images = imageBase.getImagesByUser(user)
    return render_template('gallery.html', name="Gallery", images=images)

@index.route('/upload')
@login_required
def upload():
    return render_template('upload.html', name="Uploader")

@index.route('/images/<string:filename>')
@login_required
def images(filename):
    imageBase = get_image_manager()
    user = current_user.get_id()
    if imageBase.existByUser(filename, user):
        image_binary = imageBase.getImage(filename, user)
        return send_file(image_binary, mimetype='image/jpeg', attachment_filename=filename)
    return "You can't access at this picture."

@index.route('/privacy')
def privacy():
    return render_template('privacy.html', name="Privacy")

@index.route('/logs')
def logs():
    return render_template('secret.txt', name="Secret cat plan")


