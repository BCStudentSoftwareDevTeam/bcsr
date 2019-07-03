from app.allImports import *
from app.logic import databaseInterface
import time

class GetSemesterManagement():
  '''Purpose: This class should hold any method directly related to
  systemMangement.py should be located inside of this class'''

  def __init__(self):
    # self.username = user.get_username()
    pass

  def get_years_list(self):
    '''Purpose: To create a list containing the previous year and the next
    4 years. Author: CDM 20160802
    @return {list} of strings'''
    years = []
    #Start with last year
    year  = int(time.strftime("%Y")) - 1
    for x in range(5):
      if x == 0:
        years.append(str(year))
      year += 1
      years.append(str(year))
    return years

  def create_seid(self, data):
    '''Purpose: To create the term code based off of the year, and term
    submited by form. Author: CDM 20160802
    @Param -data {immutable dict} key_values = [year,term]
    @key   -year => {string}
    @key   -term => {integer}
    '''
    print 'inside create'
    year = data['year']
    term_key  = str(data['term'])
    #same year is a list of all term keys that go off the current year,
    #instead of the previous year
    same_year = [11]
    for x in same_year:
      if int(term_key) == x:
        seid = year + term_key
      else:
        seid = str(int(year)-1) + term_key

    print "This is the SEID: " + str(seid)
    return seid

  def add_semester(self, data):
    '''Purpose: To add the semester to the database, with the correct SEID,
    and term_name given data. Author: CDM 20160802
    @Param -data {immutable dict} key_values = [year,term]
    @key   -year => {string}
    @key   -term => {integer}
    '''
    SEID          = self.create_seid(data)
    checkSeid     = Semesters.select().where(Semesters.SEID == SEID)
    term_name     = cfg['termInfo'][int(data['term'])]
    logType       = "ERROR"
    if checkSeid:
      #TODO: Log error
      message = "Semester: {0} {1} already exsists in the database.".format(term_name, data['year'])
    else:
      try:
        newSemester = Semesters(SEID = int(SEID),
                               term = term_name,
                               year = int(data['year']))
        newSemester.save(force_insert=True)
        message = "Semester: {0} {1} has been created successfully.".format(term_name, data['year'])
        logType = "INFO"
      except Exception as e:
        #TODO: Log error
        message = "An error occurred while trying to create semester {0} {1}".format(term_name, data['year'])
    return [logType,message]
