#! python3


#     ____            _____                      
#    / __ )____ _____/ /   |____  __  __________ 
#   / __  / __ `/ __  / /| /_  / / / / / ___/ _ \
#  / /_/ / /_/ / /_/ / ___ |/ /_/ /_/ / /  /  __/
# /_____/\__,_/\__,_/_/  |_/___/\__,_/_/   \___/ 

#BadAzure
# (c) NCC Group 2019                                               

################################
###         LOGGING          ###
################################

# Setup Logging
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('./log/badazure.log')
fh.setLevel(logging.DEBUG)
# Console Handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

# Imports
# Builtin Python
import json, os
# Database ORM support from PeeWee
import peewee
from peewee import StringExpression
# Web Server Imports
from werkzeug.debug import DebuggedApplication
# Flask + RESTful, Security, Admin, Marshmallow, + Playhouse Extended for Web Application
from flask import Flask, app, render_template, Request, Response, url_for, request, jsonify, redirect
from flask_restful import reqparse, abort, Api, Resource
from flask_admin import Admin, helpers as admin_helpers, AdminIndexView
from flask_security import Security, PeeweeUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user, utils, login_user
from flask_marshmallow import Marshmallow, Schema
from playhouse.shortcuts import model_to_dict, dict_to_model
# Application Imports (config, models, security and admin modules)
import config
import security
from security import User, Role, UserRoles
import models
from models import BadAzureLevel
from admin import *


# Set Up Application
logger.info('Starting Flask application...')
app = Flask(__name__)
app.config.from_object('config')
if os.environ.get('BADAZURE_SETTINGS') is not None:
    app.config.from_envvar('BADAZURE_SETTINGS')


# Check Debug Settings
logger.info('Running in {0} environment'.format(app.env))
logger.info('Debug mode is set to {0}'.format(app.debug))
if app.debug:
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

# Startup
@app.before_first_request
def before_first_request():

    # Set First-Run (Install) flag
    first_run = False

    logger.info('Running \'first request\' actions.')
    # Create the Roles "admin" and "end-user" -- unless they already exist
    logger.debug('Creating default user roles.')
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='Default User Role')
    # Create the default admin account if it doesn't already exist in the datastore.
    # In each case, use Flask-Security utility function to encrypt the password.
    logger.debug('Creating default user accounts.')
    encrypted_password = utils.encrypt_password(os.urandom(16))
    if not user_datastore.get_user('admin@badazure.com'):
        logger.warning('Did not find default user, creating...')
        first_run = True
        user_datastore.create_user(email='admin@badazure.com', password=encrypted_password)

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    logger.debug('Committing database changes.')
    models.db.commit()

    # Apply admin role to the default admin user.
    logger.debug('Adding default users to default roles.')
    user_datastore.add_role_to_user('admin@badazure.com', 'admin')
    logger.debug('Committing database changes.')
    models.db.commit()

    # If First Run then logon as admin and redirect.
    if first_run:
        logger.warning('First run of application, admin password reset required.')
        # Get ID of new admin user
        admin_user = user_datastore.get_user('admin@badazure.com')
        login_user(admin_user, False)
        return redirect(admin_user, '/admin/user/edit/?id={0}'.format(admin_user.id))


################################
###         SECURITY         ###
################################

# Create security datastore
logger.debug('Creating security datastore')
user_datastore = PeeweeUserDatastore(
    models.db, User, Role, UserRoles)
security = Security(app, user_datastore)

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


################################
###           ADMIN          ###
################################

#Admin Index View Class
class BAAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

# Set Up Admin
admin = Admin(app, name='BadAzure Admin', template_mode='bootstrap3', index_view=BAAdminIndexView())
# Add Model Views
admin.add_view(BadAzureLevelAdminView(BadAzureLevel))
# Add Flask-Admin views for Users and Roles
admin.add_view(UserAdmin(User))
admin.add_view(RoleAdmin(Role))


################################
###         ROUTES           ###
################################
# Default Route for Landing Page
@app.route("/")
def index():
    main_text = ("Welcome to BadAzure, a Microsoft Azure Security Training Platform.\n \
                            Click \'Get Started\' to explore a world of Microsoft Azure Misconfigurations and \
                            Vulnerabilities.")
    return render_template('main.html', content_main=main_text)

@app.route("/about")
def page_about():
    main_text = ("Welcome to BadAzure, a Microsoft Azure Security Training Platform.<br /> \
                            Click \'Get Started\' to explore a world of Microsoft Azure Misconfigurations and \
                            Vulnerabilities.")
    return render_template('main.html', content_main=main_text)

@app.route("/contact")
def page_contact():
    main_text = ("badazure@nccgroup.com")
    return render_template('main.html', content_main=main_text)

# Trainer Route
@app.route("/trainer/")
def trainer():
    return render_template('trainer.html')

## Error Pages

# 403 Unauthorised
@app.errorhandler(403)
def error_403_unauthorised(e):

    logger.warning('User unauthorised.')
    return redirect('/login?next={0}'.format(request.path),302)


################################
###           API            ###
################################

# Setup API
api = Api(app)
ma = Marshmallow(app)

# Define Schemas

class BadAzureLevelSchema(Schema):

    class Meta:
        fields = \
            ("level_no", "level_name", "intro_text", "level_instructions", \
            "hint_1_text", "hint_2_text", "hint_3_text", "hint_4_text", "answer_text", "references",\
            "admin_notes", "level_flag")
        
    # _links = ma.Hyperlinks(
    #     {"self": ma.URLFor("level", id="<level>"), "collection": ma.URLFor("level")}
    #)

ba_level_schema = BadAzureLevelSchema()
ba_levels_schema = BadAzureLevelSchema(many=True)

# API Responses
class BALevel(Resource):
    def get(self, level=None):  # READ
        # Check if level is specified
        if level == None:
            # Return all levels as JSON
            return jsonify(ba_levels_schema.dump(BadAzureLevel.select()))

        else:
            # Return single level as JSON
            return jsonify(ba_level_schema.dump(
                    BadAzureLevel.select().where(BadAzureLevel.level_no == level).get()))
api.add_resource(BALevel, '/api/trainer/level/', '/api/trainer/level/<int:level>', endpoint="level")


#Startup Code
if __name__ == '__main__':
    app.run(debug=True)
