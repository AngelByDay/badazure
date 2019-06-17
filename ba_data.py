# imports
from peewee import Model, SqliteDatabase
from peewee import IntegerField, CharField, TextField

db = SqliteDatabase('badazure.db')


def connect_db():

    db.connect()

    if (db.table_exists('BadAzureLevel') == False): {
        db.create_tables([BadAzureLevel,])
    }

class BadAzureLevel(Model):
    level_no = IntegerField(null=False, index=True, primary_key=True)
    level_name = CharField(null=False)
    intro_text = TextField(null=False)
    level_instructions = TextField(null=True)
    hint_1_text = TextField(null=True)
    hint_2_text = TextField(null=True)
    admin_notes = TextField(null=True)
    level_flag = CharField(null=True)

    class Meta:
        database = db