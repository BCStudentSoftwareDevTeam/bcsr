'''
This file is called by "from app import app" inside the app.py file.

It includes all the imports to be used in the app (from allImports import *).
It also includes all the application files that are used as "pages" in the app
(e.g., "from app import start" imports all the code in start.py that is behind the start.html webpage)
'''

from allImports import *
from app import allImports

# Include an import for every python file that is serving a webpage
#import your new python files here. It is not a part of the module until it is imported
from app import deadlineDisplay
from app import deadlineManagement
from app import redirectAdmin
from app import courses
from app import archive
from app import uploads
from app import deleteSyllabus
from app import download
# from app import programManagement
from app import editDivision
from app import editProgram
from app import semesterManagement
from app import userManagement
from app import errorHandler
# from app import databaseAdmin
from app import editAdmin
from app import addCourse
from app import missingSyllabi
from app import removeCourse
from app import contributors
