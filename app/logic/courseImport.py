'''
Purpose Of File: To hold all of the functions that read and check the course
list spreadsheet (.xlsx or .csv) an admin uploads when creating a new term, so
the admin can review it before any courses are imported.

Reading and checking the file does not touch the database. The caller passes
in the data that is needed (the prefix to program map and the courses that
already exist), which keeps those functions easy to test. The functions at the
bottom of the file are the exception: they hold the upload between pages and
write the term to the database. The column names and allowed file types come
from the courseImport section of config.yaml.
'''
import csv
import io
import json
import os
import re
import tempfile
import time
import uuid

from app.allImports import *

# Row statuses
OK        = 'ok'
DUPLICATE = 'duplicate'
ERROR     = 'error'

# Columns a file cannot be imported without, and how to name them to the admin
REQUIRED_COLUMNS = {'prefix':  'Subject',
                    'number':  'Course Number',
                    'section': 'Sequence'}

class CourseImportError(Exception):
  '''Purpose: Raised when the file as a whole cannot be used (wrong type,
  missing columns, empty). The message is written for the admin, so it can be
  shown as is.'''
  pass

def normalizeHeader(header):
  '''Purpose: Lowercases a column header and keeps only letters and numbers,
  so 'Course Number' and 'CRSE_NUMBER' can be compared.
  @param {string} header
  @return {string}'''
  return re.sub(r'[^a-z0-9]', '', str(header).lower())

def cleanCell(value):
  '''Purpose: Turns any cell value into a stripped string. Excel stores
  numbers as floats, so 101.0 becomes '101' and not '101.0'.
  @param value - a cell value of any type
  @return {string}'''
  if value is None:
    return ''
  if isinstance(value, float) and value.is_integer():
    return str(int(value))
  return str(value).strip()

def buildColumnMap(headers):
  '''Purpose: Finds which column of the file holds each field, using the names
  listed in config.yaml. Fields the file does not have are left out.
  @param {list} headers - the header row
  @return {dict} field => column index, plus 'instructors' => a list of
          {last, first, username} column indexes (None when missing)'''
  index = {}
  for position, header in enumerate(headers):
    index.setdefault(normalizeHeader(header), position)

  def find(names):
    for name in names:
      if name in index:
        return index[name]
    return None

  columns = {}
  for field, names in cfg['courseImport']['columns'].items():
    position = find(names)
    if position is not None:
      columns[field] = position
  columns['instructors'] = []
  for slot in cfg['courseImport']['instructorColumns']:
    columns['instructors'].append({key: find(names) for key, names in slot.items()})
  return columns

def checkRequiredColumns(columns):
  '''Purpose: Stops the upload when the file is missing columns we cannot
  import without. The raw Banner export only has instructor IDs and no
  usernames, so a missing username column gets its own message.
  @param {dict} columns - from buildColumnMap
  @raise CourseImportError'''
  missing = [name for field, name in REQUIRED_COLUMNS.items() if field not in columns]
  if missing:
    raise CourseImportError("The file is missing required column(s): {0}.".format(", ".join(missing)))
  if columns['instructors'][0]['username'] is None:
    raise CourseImportError("The file has no 'Primary Instructor Username' column. "
                            "Instructor usernames are needed to link courses to instructors.")

def readCsvRows(fileObj):
  '''Purpose: Reads every row of a csv file as a list of cells. Files saved
  by Excel are not always utf-8, so latin-1 is the fallback.'''
  data = fileObj.read()
  if isinstance(data, bytes):
    try:
      data = data.decode('utf-8-sig')
    except UnicodeDecodeError:
      data = data.decode('latin-1')
  return [row for row in csv.reader(io.StringIO(data))]

def readXlsxRows(fileObj):
  '''Purpose: Reads every row of the first sheet of an Excel workbook as a
  list of cells. Formulas are read as their last saved value.'''
  from openpyxl import load_workbook
  try:
    workbook = load_workbook(fileObj, read_only=True, data_only=True)
  except Exception:
    raise CourseImportError("The file could not be read as an Excel workbook.")
  rows = [list(row) for row in workbook.worksheets[0].iter_rows(values_only=True)]
  workbook.close()
  return rows

def parseCourseFile(fileObj, filename):
  '''Purpose: Reads a .xlsx or .csv file into a list of courses.
  @param fileObj - a file-like object (an upload or an open file)
  @param {string} filename - used to tell the file type
  @return {list} of {row: spreadsheet row number, crn, prefix, number, section,
          title, crosslist, instructors: [{username, first, last}, ...]}.
          Blank rows are dropped.
  @raise CourseImportError'''
  extension = os.path.splitext(str(filename))[1].lower().lstrip('.')
  if extension not in cfg['courseImport']['allowedExtension']:
    raise CourseImportError("Unsupported file type '{0}'. Upload a {1} file.".format(
                            extension or filename,
                            " or ".join("." + ext for ext in cfg['courseImport']['allowedExtension'])))

  raw = readXlsxRows(fileObj) if extension == 'xlsx' else readCsvRows(fileObj)
  # The header is the first row that has anything in it
  start = next((i for i, row in enumerate(raw) if any(cleanCell(c) for c in row)), None)
  if start is None:
    raise CourseImportError("The file is empty.")

  columns = buildColumnMap(raw[start])
  checkRequiredColumns(columns)

  def cell(row, position):
    if position is None or position >= len(row):
      return ''
    return cleanCell(row[position])

  courses = []
  for rowNumber, row in enumerate(raw[start + 1:], start=start + 2):
    if not any(cleanCell(c) for c in row):
      continue
    instructors = []
    for slot in columns['instructors']:
      instructors.append({'username': cell(row, slot['username']).lower(),
                          'first':    cell(row, slot['first']),
                          'last':     cell(row, slot['last'])})
    courses.append({'row':         rowNumber,
                    'crn':         cell(row, columns.get('crn')),
                    'prefix':      cell(row, columns.get('prefix')).upper(),
                    'number':      cell(row, columns.get('number')).upper(),
                    'section':     cell(row, columns.get('section')).upper(),
                    'title':       cell(row, columns.get('title')),
                    'crosslist':   cell(row, columns.get('crosslist')),
                    'instructors': instructors})
  if not courses:
    raise CourseImportError("The file has a header row but no courses.")
  return courses

def courseKey(course):
  '''Purpose: What makes a course unique within a term.
  @return {tuple} (prefix, number, section)'''
  return (course['prefix'], course['number'], course['section'])

def validateRows(courses, prefixMap, existingKeys=()):
  '''Purpose: Checks every course and sets its status and reason. Only the
  rows with the status OK should be imported. A row is skipped when
    - Subject, Course Number or Sequence is blank (error)
    - the same CRN appears earlier in the file (duplicate). Two rows can share
      a subject, number and sequence and still be different sections (private
      music lessons, for example), so that is only a duplicate when there is
      no CRN to tell them apart.
    - the course is already in the term (duplicate)
    - no program is known for its subject (error)
    - the primary instructor is missing a last name, first name or username (error)
  @param {list} courses - from parseCourseFile
  @param {dict} prefixMap - prefix => PID for the programs that exist
  @param existingKeys - courseKey of the courses already in the term
  @return {list} the same courses, each now with status, reason, warnings,
          missing (the primary instructor fields that are blank) and listed
          (the instructors to show in the preview)'''
  existing = set(existingKeys)
  seen     = {}   # courseKey => the first row that had it
  seenCrn  = {}   # crn => (row, prefix, number) of the first row that had it
  for course in courses:
    course['status']   = OK
    course['reason']   = ''
    course['warnings'] = []
    course['missing']  = []
    course['listed']   = []
    for position, slot in enumerate(course['instructors']):
      flags = [field for field in ('last', 'first', 'username') if not slot[field]]
      if position == 0:
        course['missing'] = flags
      elif not slot['username'] and (slot['first'] or slot['last']):
        course['warnings'].append("Instructor {0} {1} has no username and was not linked".format(
                                  slot['first'], slot['last']).replace("  ", " "))
      if position == 0 or slot['username'] or slot['first'] or slot['last']:
        course['listed'].append({'last': slot['last'], 'first': slot['first'], 'username': slot['username'],
                                 'missing': flags if position == 0 else []})
    course['instructors'] = [i for i in course['instructors'] if i['username']]

    blank = [name for field, name in REQUIRED_COLUMNS.items() if not course[field]]
    key   = courseKey(course)
    if blank:
      course['status'], course['reason'] = ERROR, "Missing {0}".format(", ".join(blank))
    elif key in existing:
      course['status'], course['reason'] = DUPLICATE, "{0} {1} {2} already exists in this term".format(*key)
    elif course['crn'] and course['crn'] in seenCrn:
      row, prefix, number = seenCrn[course['crn']]
      course['status'], course['reason'] = DUPLICATE, "CRN {0} is already used by {1} {2} (row {3})".format(
                                                       course['crn'], prefix, number, row)
    elif not course['crn'] and key in seen:
      course['status'], course['reason'] = DUPLICATE, "{0} {1} {2} is already listed in row {3}".format(*key, seen[key])
    elif course['prefix'] not in prefixMap:
      course['status'], course['reason'] = ERROR, "No program found for subject {0}".format(course['prefix'])
    elif course['missing']:
      names = {'last': 'Instructor Last', 'first': 'Instructor First', 'username': 'Username'}
      course['status'], course['reason'] = ERROR, "Missing values: {0}".format(
                                                   ", ".join(names[field] for field in course['missing']))
    if not blank:
      seen.setdefault(key, course['row'])
      if course['crn']:
        seenCrn.setdefault(course['crn'], (course['row'], course['prefix'], course['number']))
  return courses

def summarize(courses):
  '''Purpose: Counts the rows for the confirm and results pages.
  @param {list} courses - from validateRows
  @return {dict} total, importable, duplicates, errors, issues'''
  counts = {OK: 0, DUPLICATE: 0, ERROR: 0}
  for course in courses:
    counts[course['status']] += 1
  return {'total':      len(courses),
          'importable': counts[OK],
          'duplicates': counts[DUPLICATE],
          'errors':     counts[ERROR],
          'issues':     counts[DUPLICATE] + counts[ERROR]}

def groupByDepartment(courses, prefixMap, programNames):
  '''Purpose: Groups the rows by the department (program) that teaches them so
  the pages can show one accordion per department. A subject with no program
  gets its own group named after the subject.
  @param {list} courses - from validateRows
  @param {dict} prefixMap - prefix => PID, from getPrefixMap
  @param {dict} programNames - PID => program name
  @return {list} dicts of name, courses, importable, issues, sorted by name'''
  groups = {}
  for course in courses:
    pid  = prefixMap.get(course['prefix'].upper())
    name = programNames[pid] if pid in programNames else "{0} (no program found)".format(course['prefix'] or 'No subject')
    group = groups.setdefault(name, {'name': name, 'courses': [], 'importable': 0, 'issues': 0})
    group['courses'].append(course)
    group['importable' if course['status'] == OK else 'issues'] += 1
  return sorted(groups.values(), key=lambda group: group['name'].lower())

def getProgramNames():
  '''Purpose: Gets the name of every program.
  @return {dict} PID => program name'''
  from app.models import Programs
  return {program.PID: program.name for program in Programs.select()}

# ------------------------------------------------------------------------------
# Holding an upload between pages
# ------------------------------------------------------------------------------
# The parsed rows are too big for the session cookie, and app/static is served
# to everyone, so they are kept in the system temp folder. The session only holds
# the random token that names the file.
PENDING_MAX_AGE = 60 * 60 * 24   # seconds; older files are deleted

def getPendingFolder():
  folder = os.path.join(tempfile.gettempdir(), 'bcsr_course_import')
  os.makedirs(folder, exist_ok=True)
  return folder

def deleteOldPending():
  '''Purpose: Removes uploads that were never confirmed.'''
  folder = getPendingFolder()
  for name in os.listdir(folder):
    path = os.path.join(folder, name)
    if time.time() - os.path.getmtime(path) > PENDING_MAX_AGE:
      os.remove(path)

def getPendingPath(token):
  '''Purpose: Builds the path for a token. A token that is not 32 hex digits
  is refused, so a made up value can never point outside the folder.
  @return {string} path, or None'''
  if not isinstance(token, str) or not re.fullmatch(r'[0-9a-f]{32}', token):
    return None
  return os.path.join(getPendingFolder(), token + '.json')

def savePending(data, token=None):
  '''Purpose: Saves the data for an upload and returns its token. Pass an
  existing token to replace what is stored under it.
  @param {dict} data - must be JSON safe
  @return {string} token'''
  if token is None:
    deleteOldPending()
    token = uuid.uuid4().hex
  with open(getPendingPath(token), 'w') as pendingFile:
    json.dump(data, pendingFile)
  return token

def loadPending(token):
  '''Purpose: Gets what savePending stored.
  @return {dict} the data, or None if the token is unknown or has expired'''
  path = getPendingPath(token)
  if path is None or not os.path.exists(path):
    return None
  with open(path) as pendingFile:
    return json.load(pendingFile)

def discardPending(token):
  path = getPendingPath(token)
  if path is not None and os.path.exists(path):
    os.remove(path)

# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------
def getPrefixMap():
  '''Purpose: Maps each course prefix (e.g. CSC) to the program that already
  teaches it, based on the courses in the database. A prefix that has never
  been used has no program, so its rows are reported as errors.
  @return {dict} prefix => PID'''
  from app.models import Courses
  pairs = Courses.select(Courses.prefix, Courses.PID).distinct().tuples()
  return {str(prefix).strip().upper(): pid for prefix, pid in pairs}

def semesterExists(seid):
  from app.models import Semesters
  return Semesters.select().where(Semesters.SEID == int(seid)).exists()

def importTerm(term, year, courses, prefixMap):
  '''Purpose: Creates the semester and imports every course whose status is
  OK. The semester is created with GetSemesterManagement.add_semester and the
  courses with databaseInterface.insert_course and insert_course_user, the
  same functions the rest of the app uses.
  The semester and the courses go in as one transaction, so a failure while
  creating the semester leaves nothing behind. A course that cannot be saved
  is rolled back on its own, marked as an error, and the rest continue.
  @param {string} term - the term key from config.yaml (11, 12, 13)
  @param {string} year
  @param {list} courses - from validateRows
  @param {dict} prefixMap - from getPrefixMap
  @return {dict} imported (count), courses (with their final status), and the
          logType and message add_semester produced
  @raise CourseImportError when the semester cannot be created'''
  from app.models import mainDB, Users
  from app.logic import databaseInterface
  from app.logic.getSemesterManagement import GetSemesterManagement

  semester = GetSemesterManagement()
  seid     = int(semester.create_seid({'year': year, 'term': term}))
  imported = 0
  with mainDB.atomic():
    logType, message = semester.add_semester({'year': year, 'term': term})
    if logType == "ERROR":
      raise CourseImportError(message)
    for course in courses:
      if course['status'] != OK:
        continue
      try:
        with mainDB.atomic():
          newCourse = databaseInterface.insert_course(course['prefix'], course['number'], course['section'],
                                                      prefixMap[course['prefix']], seid)
          if not newCourse:
            raise CourseImportError("The course was not saved")
          for instructor in course['instructors']:
            user, created = Users.get_or_create(username = instructor['username'],
                                                defaults = {'firstName': instructor['first'],
                                                            'lastName':  instructor['last'],
                                                            'email':     instructor['username'] + '@berea.edu'})
            if not databaseInterface.insert_course_user(user.username, newCourse.CID):
              raise CourseImportError("The instructor was not linked to the course")
        imported += 1
      except Exception as e:
        app.logger.error("Course import failed for row {0}: {1}".format(course['row'], e))
        course['status'], course['reason'] = ERROR, "The course could not be saved"
  return {'imported': imported, 'courses': courses, 'logType': logType, 'message': message}
