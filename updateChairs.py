import os, sys
import importlib

from app.models import *
def updateDivisionChairs(username, firstName, lastName, email, did, pid):
    if pid == "none":
        try:
            rowDivision =  Users.get(Users.DID == did)
            rowDivision.DID= None
            try:
                users = Users.get(Users.username == username)
                users.DID = did
                users.save()
            except Exception as e:
                users = Users.create(username=username,firstName = firstName, lastName= lastName, email = email,  did= did)
                users.save()
        except Exception as e:
            print (e)
    elif did == "none":
        try:
            rowDivision =  Users.get(Users.DID == did)
            rowDivision.DID= None
            try:
                users = Users.get(Users.username == username)
                users.DID = did
                users.save()
            except Exception as e:
                users = Users.create(username=username,firstName = firstName, lastName= lastName, email = email,  did= did)
                users.save()
        except Exception as e:
            print (e)
    
def updateProgramChairs(username, firstName, lastName, email, pid):
    try:
        rowProgram = Users.get(Users.PID == pid)
        rowProgram.PID=  None
        try:
            users = Users.get(Users.username == username)
            users.DID = did
            users.PID = pid
            users.save()
        except Exception as e:
            users = Users.create(username=username,firstName = firstName, lastName= lastName, email = email, pid = pid)
            users.save()
    except Exception as e:
        print (e)
    
        
updateChairs("nelsonk", "Kenny","Nelson", 1, "myersco@berea.edu", 8 )
