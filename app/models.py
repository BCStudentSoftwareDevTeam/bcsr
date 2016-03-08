from peewee import *
import os
#from allImports import *   #Don't believe this import is needed for this file
# Create a database
from app.loadConfig import *

cfg       = load_config('app/config.yaml')
mainDB    = SqliteDatabase(cfg['databases']['dev'])

# Creates the class that will be used by Peewee to store the database
class dbModel (Model):
  class Meta: 
    database = mainDB

# When adding new tables to the DB, add a new class here (also add 
# to the config.yaml file)

######## CLASSES WITH NO FOREIGN KEY FIELD ########
class syllabus (dbModel):
  SID           = PrimaryKeyField()
  location      = CharField()
  
class semester (dbModel):
  SEID          = PrimaryKeyField()
  year          = IntegerField()
  term          = CharField()

class role (dbModel):
  RID           = PrimaryKeyField()
  access_level  = CharField()
  access_name   = CharField()
  
class programs (dbModel):
  PID           = PrimaryKeyField()
  name          = CharField()
  
class divisions (dbModel):
  DID           = PrimaryKeyField()
  name          = CharField()
  
class users (dbModel):
  UID           = PrimaryKeyField()
  firstname     = CharField()
  lastname      = CharField()
  username      = CharField()
  email         = CharField()



######## CLASSES WITH FOREIGN KEY FIELDS ########
class division_to_program (dbModel):
  DPID          = PrimaryKeyField()
  DID           = ForeignKeyField(divisions)
  PID           = ForeignKeyField(programs)
  
class courses (dbModel):
  CID           = PrimaryKeyField()
  cprefix       = CharField()
  cnumber       = CharField()
  PID           = ForeignKeyField(programs)  

class currentSEID (dbModel):
  CSEID         = PrimaryKeyField()
  SEID          = ForeignKeyField(semester)
  
class syllabus_course_semester (dbModel):
  XID           = PrimaryKeyField()
  SID           = ForeignKeyField(syllabus)
  CID           = ForeignKeyField(courses)
  SEID          = ForeignKeyField(semester)
  
class program_chair (dbModel):
  PCID          = PrimaryKeyField()
  PID           = ForeignKeyField(programs)
  UID           = ForeignKeyField(users)

class user_role (dbModel):
  URID          = PrimaryKeyField()
  RID           = ForeignKeyField(role)
  UID           = ForeignKeyField(users)
  
class division_chair (dbModel):
  DCID          = PrimaryKeyField()
  DID           = ForeignKeyField(divisions)
  UID           = ForeignKeyField(users)
  
class uscs (dbModel):
  QID           = PrimaryKeyField()
  XID           = ForeignKeyField(syllabus_course_semester)
  UID           = ForeignKeyField(users)