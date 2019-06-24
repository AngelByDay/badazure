# imports
import logging
from peewee import Model, SqliteDatabase
from peewee import IntegerField, CharField, TextField
from marshmallow import Schema

# Configure Logging
logger = logging.getLogger().getChild(__name__)
logger.propagate = True
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# fh = logging.FileHandler('./log/badazure.log')
# fh.setLevel(logging.DEBUG)
# # Console Handler
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# # create formatter and add it to the handlers
# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
# # add the handlers to logger
# logger.addHandler(ch)
# logger.addHandler(fh)

# Database
logger.info('Creating database connection.')
db = SqliteDatabase('badazure.db',
 pragmas={'journal_mode': 'wal',
 'cache_size': -1024 * 64})
logger.debug('Database connection: ' + str(db.connect()))

class BaseModel(Model):
     class Meta:
         database=db

class BadAzureLevel(BaseModel):
    level_no=IntegerField(null = False, index = True, primary_key = True)
    level_name=CharField(null = False)
    intro_text=TextField(null = False)
    level_instructions=TextField(null = True)
    hint_1_text=TextField(null = True)
    hint_2_text=TextField(null = True)
    hint_3_text=TextField(null = True)
    hint_4_text=TextField(null = True)
    answer_text=TextField(null = True)
    references=TextField(null = True)
    admin_notes=TextField(null = True)
    level_flag=CharField(null = True)
BadAzureLevel.create_table()
