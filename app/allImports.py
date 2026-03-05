from __future__ import print_function
'''
Include all imports in this file; it will be called at the beginning of all files.
'''

import pprint, os
from app import models
from app import *
# from models import *                # all the database models

# admin = Admin(app)

from app.loadConfig import load_config
cfg = load_config()

import sys
sys.dont_write_bytecode = True

def authUser(env):
    envK = "eppn"
    if (envK in env):
        # we need to sanitize the environment variable
        # TODO: this looks like a function that can be taken out
        return env[envK].split("@")[0].split('/')[-1].lower()
    elif ("DEBUG" in app.config) and app.config["DEBUG"]:
        old_username =  cfg["DEBUG"]["user"]
        converted_user = cfg["DEBUG"]["user"].split('@')[0].split('/')[-1].lower()
        app.logger.info(old_username+ " converted to "+ converted_user)

        return cfg["DEBUG"]["user"].split('@')[0].split('/')[-1].lower()
    else:
        return None

'''Creates the AbsolutePath based off of the relative path.
Also creates the directories in path if they are not found.
@param {string} relaitivePath - a string of directories found in config.yaml
@param {string} filename - the name of the file that should be in that directory
@return {string} filepath -returns the absolute path of the directory'''
'''TODO: ADD @PARAm for make dirs'''
def getAbsolutePath(relativePath,filename=None,makeDirs=False):
    filepath = os.path.join(sys.path[0],relativePath)
    if makeDirs == True:
        try:
            os.makedirs(filepath)
        except:
            pass
    if filename != None:
        filepath = os.path.join(filepath,filename)
    return filepath

from app import logtool
log = logtool.Log()
''' Creates an Flask object; @app will be used for all decorators.
from: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
"A decorator is just a callable that takes a function as an argument and
returns a replacement function. See start.py for an example"
'''
# app = Flask(__name__)
#from app import app

# Builds all the database connections on app run
# Don't panic, if you need clarification ask.
@app.before_request
def before_request():
    # g.dbMain =  mainDB.connect()
    pass
@app.teardown_request
def teardown_request(exception):
    dbM = getattr(g, 'db', None)
    if (dbM is not None) and (not dbM.is_closed()):
      dbM.close()
