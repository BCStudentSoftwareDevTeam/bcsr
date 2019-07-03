from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from flask import json, jsonify
from app.logic import databaseInterface

@app.route("/admin/userManagement", methods=["GET"])
def userManagement():
  if (request.method == "GET"):
      authorizedUser = AuthorizedUser()
      if authorizedUser.isAdmin:
         page        = "/" + request.url.split("/")[-1]
         users = Users.select().order_by(Users.firstName.asc())
         programs = Programs.select().order_by(Programs.name.asc())
         divisions = Divisions.select().order_by(Divisions.name.asc())
         admins = Users.select().where(Users.isAdmin == 1).order_by(Users.firstName.asc())
         return render_template("admin/userManagement/userManagement.html",
                                 divisions      = divisions,
                                 cfg           = cfg,
                                 users         = users,
                                 admins        = admins,
                                 programs      = programs,
                                 isAdmin       = authorizedUser.isAdmin)
      else:
         abort(403)

@app.route("/admin/userInsert", methods = ["POST"])
def user_insert():
    if request.form.get('adduser') == 'adduser':
        if request.form.get('accessType') == "program_chair":
            add_program_chair(request)
        elif request.form.get('accessType') == 'division_chair':
            add_division_chair(request)
        elif request.form.get('accessType') == 'administrator' :
            add_administrator(request)
    #for updating removed users
    elif request.form.get('removeuser') == 'removeuser':
        if request.form.get('accessType') == "program_chair":
            remove_program_chair(request)
        elif request.form.get('accessType') == 'division_chair':
            remove_division_chair(request)
        elif request.form.get('accessType') == 'administrator' :
            remove_administratorr(request)
    return redirect(url_for("userManagement"))

def add_program_chair(request):
    newChairs   = request.form.get("userToAdd")
    PID =request.form.get("program")
    newChair  = Users.get(Users.username == newChairs)
    newChair.PID = PID
    newChair.save()
    message = "USER: {0} has been added as a program chair for pid: {1}".format(newChairs,PID)
    app.logger.info(message)
    flash("Program chair successfully added.")

def add_division_chair(request):
    newChairs    = request.form.get("userToAdd")
    DID          = request.form.get("division")
    newChair     = Users.get(Users.username == newChairs)
    newChair.DID = DID
    newChair.save()
    message      = "USER: {0} has been added as a division chair for did: {1}".format(newChairs,DID)
    app.logger.info(message)
    flash("Division chair successfully added.")

def add_administrator(request):
    newAdmins   = request.form.get("userToAdd")
    newAdmin    = Users.get(Users.username == newAdmins)
    newAdmin.isAdmin = 1
    newAdmin.save()
    message     = "USER: {0} has been added as an admin".format(newAdmins)
    app.logger.info(message)
    flash("Admin successfully added.")

def remove_program_chair(request):
    chair_to_remove  =  request.form.get("userToRemove")
    PID              =  request.form.get("program")
    program_chair = Users.get(Users.username == request.form.get("userToRemove"), Users.PID== request.form.get("program"))
    program_chair.delete_instance()
    message = "USER: {0} has been removed as a program chair for pid: {1}".format(chair_to_remove ,PID)
    app.logger.info(message)
    flash("Program chair successfully removed.")

def remove_division_chair(request):
    division_to_remove = request.form.get("userToRemove")
    DID                = request.form.get("division")
    division_chair      = Users.get(Users.username == request.form.get("userToRemove"), Users.DID== request.form.get("division"))
    division_chair.delete_instance()
    message = "USER: {0} has been removed as a division chair for did: {1}".format(division_to_remove ,DID)
    app.logger.info(message)
    flash("Division chair successfully removed.")

def remove_administratorr(request):
    user = Users.get(Users.username == request.form.get("userToRemove"))
    user.isAdmin = 0
    user.save()
    message = "USER: {0} has been removed as an administrator".format(user)
    app.logger.info(message)
    flash("Administrator successfully removed.")

@app.route("/admin/userManagement/get_admin", methods = ["GET"])
def administrators():
    alladmin = Users.select().where(Users.isAdmin == 1)
    newadmin={}
    for admin in alladmin:
        newadmin[admin.username]={'firstname':admin.firstName,
                        'lastname':admin.lastName,
                        'username':admin.username
        }
    return json.dumps(newadmin)

@app.route('/admin/userManagement/get_program_chairs/<program>', methods = ["GET"])
def program_chair(program):
    allchairs = Users.select().where(Users.PID==program)
    newchairs={}
    for chair in allchairs:
        newchairs[chair.username]={'firstname':chair.firstName,
                        'lastname':chair.lastName,
                        'username':chair.username
        }
    return json.dumps(newchairs)

@app.route('/admin/userManagement/get_division_chairs/<division>',methods=["GET"])
def get_divisions_json(division):
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin:
        chairs = Users.select().where(Users.DID == division)
        chairList = {}
        for chair in chairs:
            chairList[chair.username]={'firstname':chair.firstName,
                            'lastname':chair.lastName,
                            'username':chair.username
            }

        return json.dumps(chairList)
