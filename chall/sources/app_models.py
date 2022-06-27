#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, UserMixin, RoleMixin

db = SQLAlchemy()

# Users login

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.Text())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250))
    password = db.Column(db.String(250))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )


def init_user_datastore():
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    return user_datastore

def create_models(app):
    db.init_app(app)
    app.app_context().push()
    db.create_all()
