'''
Adds an individual user to the database.
'''
import os, sys
import importlib

# Don't forget to import your own models!
from app.models import *

#######
#USERS#
#######
users     = Users(      firstName = "Ruoxi",
                        lastName  = "Zhang",
                        username  = "zhangr",
                        email     = "zhangr@berea.edu",
                        isAdmin     = False
                  ).save(force_insert=True)

