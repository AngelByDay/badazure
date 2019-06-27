from flask import Flask, render_template
from peewee import Database
from peewee import *
from models import BaseModel
from flask_security import Security, PeeweeUserDatastore, \
    UserMixin, RoleMixin, login_required
import logging

# Configure Logging
# Configure Logging
logger = logging.getLogger().getChild(__name__)
logger.propagate = True

class Role(BaseModel, RoleMixin):
    name = CharField(unique=True)
    description = TextField(null=True)

def __str__(self):
    return self.name

try:
    logger.info('Creating role table.')
    Role.create_table()
except Exception as err:
    logger.error(err)

class User(BaseModel, UserMixin):
    email = TextField(unique=True)
    display_name = TextField(null=True)
    password = TextField()
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)

    def __str__(self):
        return '{0} ({1})'.format(self.display_name, self.email)

try:
    logger.info('Creating user table.')
    User.create_table()
except Exception as err:
    logger.error(err)

class UserRoles(BaseModel):
    # Because peewee does not come with built-in many-to-many
    # relationships, we need this intermediary class to link
    # user to roles.
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)
try:
    logger.info('Creating user roles table.')
    UserRoles.create_table()
except Exception as err:
    logger.error(err)