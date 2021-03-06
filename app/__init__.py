'''
This file is called by "from app import app" inside the app.py file.

It includes all the imports to be used in the app (from allImports import *).
It also includes all the application files that are used as "pages" in the app
(e.g., "from app import start" imports all the code in start.py that is behind the start.html webpage)
'''
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import g
from flask import url_for
from flask import flash
from flask import abort
from flask_admin import Admin

app = Flask(__name__)

# from allImports import *
from app import allImports
from app.loadConfig import load_config

secret_cfg = load_config("app/secret_config.yaml")
app.secret_key = secret_cfg["secret_key"]

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
from app import divisionManagement
from app import programManagement
from app import semesterManagement
from app import errorHandler
from app import addCourse
from app import missingSyllabi
from app import removeCourse
from app import contributors
from app import userManagement
