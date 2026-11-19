from peewee import *
import os
import datetime
import re
from app.loadConfig import load_config


secret_cfg = load_config('app/secret_config.yaml')
mainDB = MySQLDatabase(secret_cfg['db']['db_name'],
                       host = secret_cfg['db']['host'],
                       user = secret_cfg['db']['username'],
                       passwd = secret_cfg['db']['password'])

# FOR USE IN MIGRATING FROM SQLITE TO SQL ONLY!
#mainDB = SqliteDatabase("data/bcsr.sqlite", pragmas = (('busy_timeout', 100), ('journal_mode', 'WAL')))

# Creates the class that will be used by Peewee to store the database
class dbModel (Model):
  class Meta:
    database = mainDB

'''
When adding a new table to the DB, add a new class here (also add
it to the config.yaml file)
Class Style Structure
--------------------------------------------------------------------------------
Data               | Style                       | Example
--------------------------------------------------------------------------------
Class Names        | CAP Case                     |  Ex. Semester
Primary Keys       | All Caps                     |  Ex. SEID
ForeignKeyField    | All Caps (Same as other key) |  Ex. Divisions.DID = Programs.DID
Variables in Class | Mixed Case                   |  Ex. filePath
--------------------------------------------------------------------------------
'''

# CLASSES WITH NO FOREIGN KEY FIELD
class Semesters (dbModel):
  SEID          = PrimaryKeyField()
  year          = IntegerField()
  term          = CharField()

  def __str__(self):
    return str(self.SEID)

class Divisions (dbModel):
  DID           = PrimaryKeyField()
  name          = CharField()
  def __str__(self):
    return str(self.DID)

# CLASSES WITH FOREIGN KEY FIELDS
class Programs (dbModel):
  PID           = PrimaryKeyField()
  name          = CharField()
  DID           = ForeignKeyField(Divisions)

  def __str__(self):
    return str(self.PID)

class Users (dbModel):
  username      = CharField(primary_key=True)
  firstName     = CharField()
  lastName      = CharField()
  email         = CharField()
  isAdmin       = BooleanField(default = False)
  PID           = ForeignKeyField(Programs,  null = True)   # indicates I'm a Program Chair
  DID           = ForeignKeyField(Divisions, null = True)   # indicates I'm a Division Chair

  def __str__(self):
    return self.username

class Courses (dbModel):
  CID           = PrimaryKeyField()
  prefix        = CharField()
  number        = CharField()
  section       = CharField()
  PID           = ForeignKeyField(Programs)
  SEID          = ForeignKeyField(Semesters)
  filePath      = TextField(null = True)
  lastModified  = TextField(null = True)

  def __str__(self):
    return str(self.CID)

class UsersCourses (dbModel):
  UCID          = PrimaryKeyField()
  username      = ForeignKeyField(Users)
  CID           = ForeignKeyField(Courses)

class Deadline(dbModel):
  description  = TextField()
  date         = DateField()

class ActivityLog(dbModel):
  timestamp    = DateTimeField(default=datetime.datetime.now)
  actor        = CharField()
  action       = TextField()

  @classmethod
  def simplify_action(cls, action):
    action = str(action).strip()

    match = re.match(r'^Semester:\s*(.+?)\s+(\d{4})\s+has been created successfully\.?$', action, re.I)
    if match:
      return "Created {0} {1}".format(match.group(1).lower(), match.group(2))

    match = re.match(r'^Deadline:\s*(.*?)\s+has been (added|deleted)\.?$', action, re.I)
    if match:
      verb = "Created" if match.group(2).lower() == "added" else "Deleted"
      return "{0} deadline {1}".format(verb, match.group(1))

    match = re.match(r'^Deadline:\s*has been edited to\s*(.*?)\.?$', action, re.I)
    if match:
      return "Edited deadline {0}".format(match.group(1))

    match = re.match(r'^The course\s+\(([^)]+)\)\s+has been deleted\.?$', action, re.I)
    if match:
      return "Deleted course {0}".format(match.group(1))

    match = re.match(r'^Course:\s*(.+?)\s+has been added$', action, re.I)
    if match:
      return "Added course {0}".format(match.group(1))

    match = re.match(r'^Uploads:\s*(.+?)\s+has been (uploaded|deleted)$', action, re.I)
    if match:
      verb = "Uploaded" if match.group(2).lower() == "uploaded" else "Deleted"
      filename = os.path.basename(match.group(1))
      return "{0} syllabus {1}".format(verb, filename)

    match = re.match(r'^USER:\s*(\S+)\s+has been (added|removed) as (?:a )?(.+)$', action, re.I)
    if match:
      verb = "Added" if match.group(2).lower() == "added" else "Removed"
      role = match.group(3)
      role = re.sub(r'\s+for pid:\s*\S+$', '', role, flags=re.I)
      role = re.sub(r'\s+for did:\s*\S+$', '', role, flags=re.I)
      role = re.sub(r'^an?\s+', '', role, flags=re.I)
      role = role.strip()
      return "{0} {1} {2}".format(verb, role, match.group(1))

    match = re.match(r'^Download:\s*(.+?)\s+has been downloaded(?: as a zip)?$', action, re.I)
    if match:
      return "Downloaded {0}".format(os.path.basename(match.group(1)))

    match = re.match(r'^Semester:\s*(.+?)\s+already exists in the database\.?$', action, re.I)
    if match:
      return "Semester already exists: {0}".format(match.group(1))

    return action

  @property
  def clean_action(self):
    return self.simplify_action(self.action)
