# imports
import logging
from peewee import Model, SqliteDatabase
from peewee import IntegerField, CharField, TextField
from marshmallow import Schema

# Configure Logging
logger = logging.getLogger(__name__)

#Database
logger.info('Creating database connection.')
db = SqliteDatabase('badazure.db')
logger.debug('Database connection ' + str(db.connect()))

class BaseModel(Model):
     class Meta:
         database = db

class BadAzureLevel(BaseModel):
    level_no = IntegerField(null=False, index=True, primary_key=True)
    level_name = CharField(null=False)
    intro_text = TextField(null=False)
    level_instructions = TextField(null=True)
    hint_1_text = TextField(null=True)
    hint_2_text = TextField(null=True)
    hint_3_text = TextField(null=True)
    hint_4_text = TextField(null=True)
    answer_text = TextField(null=True)
    references = TextField(null=True)
    admin_notes = TextField(null=True)
    level_flag = CharField(null=True)