# imports
import app
from peewee import Model, SqliteDatabase
from peewee import IntegerField, CharField, TextField

#Database
db = SqliteDatabase('./app/badazure.db')

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
    admin_notes = TextField(null=True)
    level_flag = CharField(null=True)