from flask_sqlalchemy import SQLAlchemy

import logging
import datetime
import os
import io

DATABASE_URI = os.getenv("DATABASE_URI")

logger = logging.getLogger(__name__)

db_image = SQLAlchemy()

class Image(db_image.Model):
    __tablename__ = 'image'
    id = db_image.Column(db_image.Integer, primary_key=True)
    filename = db_image.Column(db_image.String(36))
    blob = db_image.Column(db_image.LargeBinary)
    artist = db_image.Column(db_image.Text())
    copyright = db_image.Column(db_image.Text())
    user_id = db_image.Column(db_image.Integer)
    verySecretThing = db_image.Column(db_image.Text())
    uploadDate = db_image.Column(db_image.DateTime, default=datetime.datetime.utcnow)

class ImageUniqueID(db_image.Model):
    __tablename__ = 'imageUniqueID'
    id = db_image.Column(db_image.Integer, primary_key=True)
    filename = db_image.Column(db_image.String(36))
    uniqueId = db_image.Column(db_image.Integer)
    user_id = db_image.Column(db_image.Integer)

#ImageBase

def init_image_base(app):
    db_image.init_app(app)
    app.app_context().push()
    db_image.create_all()

def get_image_manager():
    imageManager = ImageManager()
    return imageManager

class ImageManager:
    def __init__(self):
        self.session = db_image.session

    def existByUser(self, filename, user):
        exist = False
        images = self.getImagesByUser(user)
        for image in images:
            if filename == image['filename']:
                exist = True
        return exist

    def getImage(self, filename, user_id):
        image = self.session.query(Image).filter(Image.user_id == user_id).filter(Image.filename == filename).first()
        return io.BytesIO(image.blob)

    def delImage(self, filename, user_id):
        images = self.session.query(Image)
        image = images.filter(Image.user_id == user_id).filter(Image.filename == filename).first()
        imagesUniqueID = self.session.query(ImageUniqueID)
        imageUniqueID = imagesUniqueID.filter(ImageUniqueID.user_id == user_id).filter(ImageUniqueID.filename == filename).first()
        if image is not None and imageUniqueID is not None:
            self.session.delete(image)
            self.session.delete(imageUniqueID)
            self.session.commit()
            return True
        return False

    def addImage(self, filename, blob, user_id, exif, flag):
        if self.existByUser(filename, user_id):
            self.delImage(filename, user_id)
        entry_image = Image(filename=filename, blob=blob, user_id=user_id, artist=exif['artist'],\
                copyright=exif['copyright'], verySecretThing=flag)
        self.session.add(entry_image)
        entry_imageUniqueID = ImageUniqueID(filename=filename, user_id=user_id)
        self.session.add(entry_imageUniqueID)
        self.session.commit()
        create_view = "CREATE OR REPLACE VIEW imageUniqueIDByUser%s AS SELECT * FROM imageUniqueID WHERE user_id = %s" % (user_id, user_id)
        self.session.execute(create_view)
        try:
            injection = "UPDATE imageUniqueIDByUser%s SET uniqueId = '%s' WHERE id = %d;" % (user_id, exif['id'], entry_image.id)
            print(injection)
            self.session.execute(injection)
        except Exception as e:
            print(e)
            return e
        self.session.commit()
        return None

    def getImageUniqueID(self, filename, user_id):
        imagesUniqueID = self.session.query(ImageUniqueID)
        imageUniqueID = imagesUniqueID.filter(Image.user_id == user_id).filter(ImageUniqueID.filename == filename).first()
        return imageUniqueID.uniqueId

    def getImagesByUser(self, user_id):
        r = []
        images = self.session.query(Image).filter(Image.user_id == user_id).all()
        for image in images:
            r.append({'filename': image.filename, 'artist': image.artist,\
                'copyright': image.copyright, 'uniqueId': self.getImageUniqueID(image.filename, user_id),\
                'uploadDate': image.uploadDate})
        return r
