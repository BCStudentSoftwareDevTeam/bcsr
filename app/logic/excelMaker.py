import xlsxwriter
import sys, os

from app.allImports import *
from app.models import *

def makeExcelFile(SEID):
    filename = "bcsr-{}-missing-syllabi.xlsx".format(SEID)
    path = getAbsolutePath(cfg['fileOperations']['dataPaths']['tmp'],filename,True)
    workbook = xlsxwriter.Workbook(path)
    workbook.set_properties({
        'title':    'Missing Syllabi for {}'.format(SEID),
        'author':   'Cody Myers',
        'comments': 'Created with Python and XlsxWriter'
    })
    master_worksheet = workbook.add_worksheet('All Courses')
    master_worksheet.write('A1','Username')
    master_worksheet.write('B1', 'First Name')
    master_worksheet.write('C1', 'Last Name')
    master_worksheet.write('D1', 'Email')
    master_worksheet.write('E1', 'Course(s)')
    master_row = 2
    users = UsersCourses.select(UsersCourses.username).distinct().join(Courses).where(
                                    Courses.filePath >> None,
                                    Courses.SEID== SEID).order_by(
                                                            UsersCourses.username)
    for user in users:
        master_worksheet.write('A{}'.format(master_row),user.username.username)
        master_worksheet.write('B{}'.format(master_row),user.username.firstName)
        master_worksheet.write('C{}'.format(master_row),user.username.lastName)
        master_worksheet.write('D{}'.format(master_row),user.username.email)
        courses = UsersCourses.select().join(Courses).where(
                    UsersCourses.username == user.username.username,
                    Courses.filePath >> None,
                    Courses.SEID == SEID)
        colLetter = 'D'
        for c in courses:
            colLetter = chr(ord(colLetter) + 1)
            #Turns value in to next letter up
            #E.G. D -> E
            colName   = colLetter + '{}'
            course_info = c.CID.prefix+'-'+c.CID.number+'-'+c.CID.section
            master_worksheet.write(colName.format(master_row),course_info)
        master_row  += 1
    workbook.close()
    print(path)
    return path
