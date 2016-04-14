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
###########################CLASSES#############################
#Class Names        -> Camel Case                                         Ex. Semester
#Primary Keys       -> All Caps                                           Ex. SEID
#ForeignKeyField    -> Same Name as Key being related to                  Ex. Divisions.DID = Programs.DID
#Variables in Class -> Mixed Case                                         Ex. filePath


######## CLASSES WITH NO FOREIGN KEY FIELD ########
class Semesters (dbModel):
  SEID          = PrimaryKeyField()
  year          = IntegerField()
  term          = CharField()
  current       = BooleanField(default = False)
 
class Divisions (dbModel):
  DID           = PrimaryKeyField()
  name          = CharField()
  
######## CLASSES WITH FOREIGN KEY FIELDS ########
class Programs (dbModel):
  PID           = PrimaryKeyField()
  name          = CharField()
  DID           = ForeignKeyField(Divisions)
  
class Users (dbModel):
  UID           = PrimaryKeyField()
  firstName     = CharField()
  lastName      = CharField()
  userName      = CharField()
  email         = CharField()
  admin         = BooleanField(default = False)
  PID           = ForeignKeyField(Programs,  null = True)
  DID           = ForeignKeyField(Divisions, null = True)
  
class Courses (dbModel):
  CID           = PrimaryKeyField()
  prefix        = CharField()
  number        = CharField()
  section       = CharField()
  PID           = ForeignKeyField(Programs)
  SEID          = ForeignKeyField(Semesters)
  filePath      = TextField(null = True)
  lastModified  = TextField(null = True)
  
class UsersCourses (dbModel):
  UCID          = PrimaryKeyField()
  userName      = ForeignKeyField(Users, to_field = "userName")
  CID           = ForeignKeyField(Courses)