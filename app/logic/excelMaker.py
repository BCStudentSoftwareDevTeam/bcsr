import xlsxwriter
from app.allImports import *
import sys

def makeExcelFile(SEID):
    filename = "bcsr-{}-missing-syllabi.xlsx".format(SEID)
    path = getAbsolutePath(cfg['fileOperations']['dataPaths']['tmp'],filename,False)
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
    master_worksheet.write('E1', 'Course')
    master_row = 2
    
    courses = UsersCourses.select().join(Courses).where(
                                    Courses.filePath >> None,
                                    Courses.SEID== SEID).order_by(
                                                            UsersCourses.username)
    for c in courses:
        course_info = c.CID.prefix+'-'+c.CID.number+'-'+c.CID.section
        #Add to master worksheet
        master_worksheet.write('A{}'.format(master_row),c.username.username)
        master_worksheet.write('B{}'.format(master_row),c.username.firstName)
        master_worksheet.write('C{}'.format(master_row),c.username.lastName)
        master_worksheet.write('D{}'.format(master_row),c.username.email)
        master_worksheet.write('E{}'.format(master_row),course_info)
        master_row  += 1
    workbook.close()
    return path
    
    
    
    