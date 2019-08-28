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
    # mainDB.create_tables(Prefixes),
    Prefixes.create_table()
    )
except Exception as e:
    print("Table Prefixes already exists.")
    print(e)
    print("I'm below here")

# Populated new table "Prefixes" with our desired data
try:
    state_1 = Prefixes.create(prefix = 'BIO', PID = 11)
    state_2 = Prefixes.create(prefix = "CHM", PID = 12);
    state_3 = Prefixes.create(prefix = "MAT", PID = 13);
    state_4 = Prefixes.create(prefix = "NUR", PID = 14);
    state_5 = Prefixes.create(prefix = "PHY", PID = 15);
    state_6 = Prefixes.create(prefix = "ANR", PID = 16);
    state_7 = Prefixes.create(prefix = "CSC", PID = 17);
    state_8 = Prefixes.create(prefix = "BUS", PID = 18);
    state_9 = Prefixes.create(prefix = "ECO", PID = 18);
    state_10 = Prefixes.create(prefix = "SENS", PID = 19);
    state_11 = Prefixes.create(prefix = "TAD", PID = 20);
    state_12 = Prefixes.create(prefix = "CFS", PID = 21);
    state_13 = Prefixes.create(prefix = "HHP", PID = 22);
    state_14 = Prefixes.create(prefix = "HLT", PID = 22);
    state_15 = Prefixes.create(prefix = "WELL", PID = 22);
    state_16 = Prefixes.create(prefix = "PSY", PID = 23);
    state_17 = Prefixes.create(prefix = "SOC", PID = 24);
    state_18 = Prefixes.create(prefix = "COM", PID = 25);
    state_19 = Prefixes.create(prefix = "ENG", PID = 26);
    state_20 = Prefixes.create(prefix = "CHI", PID = 27);
    state_21 = Prefixes.create(prefix = "FRN", PID = 27);
    state_22 = Prefixes.create(prefix = "GER", PID = 27);
    state_23 = Prefixes.create(prefix = "JPN", PID = 27);
    state_24 = Prefixes.create(prefix = "LAT", PID = 27);
    state_25 = Prefixes.create(prefix = "SPN", PID = 27);
    state_26 = Prefixes.create(prefix = "HEB", PID = 27);
    state_27 = Prefixes.create(prefix = "MUA", PID = 28);
    state_28 = Prefixes.create(prefix = "MUS", PID = 28);
    state_29 = Prefixes.create(prefix = "THR", PID = 29);
    state_30 = Prefixes.create(prefix = "ARH", PID = 30);
    state_31 = Prefixes.create(prefix = "ART", PID = 30);
    state_32 = Prefixes.create(prefix = "AST", PID = 31);
    state_33 = Prefixes.create(prefix = "HIS", PID = 32);
    state_34 = Prefixes.create(prefix = "PHI", PID = 33);
    state_35 = Prefixes.create(prefix = "PSC", PID = 34);
    state_36 = Prefixes.create(prefix = "REL", PID = 35);
    state_37 = Prefixes.create(prefix = "LES", PID = 42);
    state_38 = Prefixes.create(prefix = "AFR", PID = 36);
    state_39 = Prefixes.create(prefix = "APS", PID = 37);
    state_40 = Prefixes.create(prefix = "EDS", PID = 38);
    state_41 = Prefixes.create(prefix = "PSJ", PID = 39);
    state_42 = Prefixes.create(prefix = "WGS", PID = 40);
    state_43 = Prefixes.create(prefix = "GST", PID = 41);
    state_44 = Prefixes.create(prefix = "GSTR", PID = 41);
    state_45 = Prefixes.create(prefix = "GEO", PID = 43);
    state_46 = Prefixes.create(prefix = "CLS", PID = 27);
    print("I saved all the data entries.")
except Exception as e:
    print("I did not save the data.")
    print(e)

# Renamed the table "Courses" to "Courses_old" to hold our data from the
class Courses_old (dbModel):
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

migrate(
migrator.rename_table('Courses', 'Courses_old'),
)

# Created our new "Courses" table
try:
    migrate(
    # mainDB.create_tables(Courses),
    Courses.create_table()
    )
except Exception as e:
    print("Table Courses already exists.")
    print(e)

# Deleted one entry in the "Courses_old" table because the SIED read "201615"
#   because this SIED is no longer used and caused us issues. The program would
#   accidently deleted another entry as well, so we just placed the correct
#   entry back into the table.
q = Courses_old.select()
for row in q:
   if (row.number == "498" and row.prefix == "COM" and row.section == "A"):
       row.delete_instance()
       try:
           com498 = Courses_old.create(CID = 12752, prefix = "COM", number = "498", section = "A", PID = 25, SEID = 201712)
       except Exception as e:
           print("COM 498 already exist")

# Copied all the data from the "Courses_old" table into the new "Courses" table
try:
    q = Courses_old.select()
    for row in q:
        Courses.create(CID = row.CID, prefix = row.prefix, number = row.number, section = row.section, PID = row.PID, SEID = row.SEID, filePath = row.filePath, lastModified = row.lastModified)
except Exception as e:
    print(e)

# Deleted the table "Courses_old" from our database
try:
    migrate(
    # mainDB.drop_tables(Courses_old),
    Courses_old.drop_table()
    )
except Exception as e:
    print(e)

# Added the new indexes to our database
try:
    migrate(
    migrator.add_index('prefixes', ('PID_id',)),
    migrator.add_index('courses', ('prefix_id',)),
    migrator.add_index('courses', ('PID_id',)),
    migrator.add_index('courses', ('SEID_id',)),
    )
except Exception as e:
    print(e)

try:
    allWell = Courses.select().join_from(Courses, Prefixes).where(Courses.prefix.prefix == "WELL")
    for i in allWell:
        if i.filePath != None:
            x = i.filePath
            x = x.replace("DivisionIV", "DivisionIII")
            # print(x)
            # print(i.filePath)
            query = Courses.update(filePath = x).where(Courses.CID == i.CID)
            query.execute()
except Exception as e:
    print(e)
