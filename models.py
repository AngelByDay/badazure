from peewee import Model
from peewee import IntegerField, CharField, TextField

import ba_data

class BadAzureLevel(Model):
    level_no = IntegerField(null=False, index=True, primary_key=True)
    level_name = CharField(null=False)
    intro_text = TextField(null=False)
    level_instructions = TextField(null=False)
    hint_1_text = TextField(null=True)
    hint_2_text = TextField(null=True)

    class Meta:
        database = ba_data.db
