from flask import Flask, render_template
from peewee import Database
from peewee import *
from models import BaseModel
from flask_security import Security, PeeweeUserDatastore, \
    UserMixin, RoleMixin, login_required

class Role(BaseModel, RoleMixin):
    name = CharField(unique=True)
    description = TextField(null=True)

class User(BaseModel, UserMixin):
    email = TextField()
    password = TextField()
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)

class UserRoles(BaseModel):
    # Because peewee does not come with built-in many-to-many
    # relationships, we need this intermediary class to link
    # user to roles.
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)