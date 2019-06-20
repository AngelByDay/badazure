#! python3


#    ____            _____                      
#   / __ )____ _____/ /   |____  __  __________ 
#  / __  / __ `/ __  / /| /_  / / / / / ___/ _ \
# / /_/ / /_/ / /_/ / ___ |/ /_/ /_/ / /  /  __/
#/_____/\__,_/\__,_/_/  |_/___/\__,_/_/   \___/ 

#BadAzure
# (c) NCC Group 2019                                               


# Imports
import logging
from flask import Flask, app, render_template, Request, Response, url_for
from flask_restful import reqparse, abort, Api, Resource
from flask_admin import Admin, helpers as admin_helpers, AdminIndexView
from flask_security import Security, PeeweeUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user, utils
from playhouse.shortcuts import model_to_dict, dict_to_model
import models
from models import BadAzureLevel
from ba_security import User, UserRoles, Role
from ba_admin import *
import json

################################
###         LOGGING          ###
################################

# Setup Logging
logger = logging.getLogger(__name__)
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


# Set Up Application
logger.info('Starting Flask application...')
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = 'b7c3ae49e6d8b3290a0eff32a9a7b4ccceae7b3f'
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config['SECURITY_PASSWORD_SALT'] = 'bser345o9823bcy8bs36874edbn8yw4rc25466tycu'

# Startup
@app.before_first_request
def before_first_request():

    logger.info('Running \'first run\' actions.')

    # Create any database tables that don't exist yet.
    logger.debug('Creating database tables.')
    models.db.create_tables([BadAzureLevel, Role, UserRoles, User ])

    # Create the Roles "admin" and "end-user" -- unless they already exist
    logger.debug('Creating default user roles.')
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='user', description='Default User Role')
    # Create two Users for testing purposes -- unless they already exists.
    # In each case, use Flask-Security utility function to encrypt the password.
    logger.debug('Creating default user accounts.')
    encrypted_password = utils.encrypt_password('password')
    if not user_datastore.get_user('someone@example.com'):
        user_datastore.create_user(email='someone@example.com', password=encrypted_password)
    if not user_datastore.get_user('admin@example.com'):
        user_datastore.create_user(email='admin@example.com', password=encrypted_password)

    # Commit any database changes; the User and Roles must exist before we can add a Role to the User
    logger.debug('Committing database changes.')
    models.db.commit()

    # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
    # Users already have these Roles.) Again, commit any database changes.
    logger.debug('Adding default users to default roles.')
    user_datastore.add_role_to_user('someone@example.com', 'user')
    user_datastore.add_role_to_user('admin@example.com', 'admin')
    logger.debug('Committing database changes.')
    models.db.commit()


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
        return current_user.is_authenticated # This does the trick rendering the view only if the user is authenticated

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
    return render_template('main.html')

# Trainer Route
@app.route("/trainer/")
def trainer():
    return render_template('trainer.html')


################################
###           API            ###
################################

# Setup API
api = Api(app)

# API Responses

class BALevel(Resource):
    def get(self, level):  # READ
        ba_level = None
        try:
            ba_level = BadAzureLevel.select().where(BadAzureLevel.level_no == level).get()
        except:
            print('An error ocurred.')
        if ba_level == None:
            return Response(status=404)
        else:
            return Response(response=json.dumps(model_to_dict(ba_level)), status=200, mimetype='application/json')
api.add_resource(BALevel, '/api/trainer/level/<int:level>')


#Startup Code
if __name__ == '__main__':
    app.run(debug=True)
