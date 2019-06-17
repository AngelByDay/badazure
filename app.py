#! python3

# Imports
from flask import Flask, app, render_template, Request, Response
from flask_restful import reqparse, abort, Api, Resource
from flask_admin import Admin
from playhouse.shortcuts import model_to_dict, dict_to_model
import ba_data
from ba_admin import *
from models import BadAzureLevel
import json

# Set Up Application

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SECRET_KEY'] = 'b7c3ae49e6d8b3290a0eff32a9a7b4ccceae7b3f'
api = Api(app)

#Database Connection
ba_data.connect_db()

# Set Up Admin
admin = Admin(app, name='BadAzure', template_mode='bootstrap3')
admin.add_view(BadAzureLevelAdminView(BadAzureLevel))


# Default Route for Landing Page
@app.route("/")
def index():
    return render_template('main.html')


@app.route("/trainer/")
def trainer():
    return render_template('trainer.html')


# API Routes

class BALevel(Resource):
    def get(self, level):   #READ
        ba_level = BadAzureLevel.select().where(BadAzureLevel.level_no == level).get()
        if ba_level == None:
            return Response(status=404)
        else:
            return Response(response=json.dumps(model_to_dict(ba_level)), status=200, mimetype='application/json')

    # def post(self, level):  #CREATE
    #     ba_level = BadAzureLevel.create(level_no=request.json['level_no'],
    #                                     level_name=request.json['level_name'],
    #                                     intro_text=request.json['intro_text'],
    #                                     level_instructions=request.json['level_instructions'])
    #     return json.dumps(model_to_dict(ba_level)), 201
    
    # def put(self, level):   #UPDATE
    #     ba_level = BadAzureLevel.select().where(BadAzureLevel.level_no == level).get()
    #     if ba_level == None:
    #         return Response(status=404)
    #     else:
    #         ba_level.level_name = request.json['level_name']
    #         ba_level.intro_text = request.json['intro_text']
    #         ba_level.level_instructions = request.json['level_instructions']
    #         ba_level.save()
    #         return json.dumps(model_to_dict(ba_level)), 200



api.add_resource(BALevel, '/api/trainer/level/<int:level>')


if __name__ == '__main__':
    app.run(debug=True)

    ba_data.connect_db()
