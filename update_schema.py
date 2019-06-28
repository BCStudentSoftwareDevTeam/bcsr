from peewee import *
from playhouse.migrate import *
from app.models import *
from app.loadConfig import load_config


here = os.path.dirname(__file__)
cfg       = load_config(os.path.join(here,'app/config.yaml'))
db        = os.path.join(here,cfg['databases']['dev'])

mainDB = SqliteDatabase (db)

class dbModel (Model):
   class Meta:
       database = mainDB

migrator = SqliteMigrator(mainDB)

# Created the new table "Prefixes" in database
try:
   migrate(
   migrator.add_column("Semesters", "box_folders", CharField(null=True))
   )
except Exception as e:
   print("Column box_folders already exists on table Semesters")
   print(e)
