from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from flask import json, jsonify
from app.logic import databaseInterface

@app.route("/admin/userManagement", methods=["GET"])
def userManagement():
  if (request.method == "GET"):
      authorizedUser = AuthorizedUser()
      # only admin should be able to change division chairs
      if authorizedUser.isAdmin:
         page        = "/" + request.url.split("/")[-1]
         users = Users.select().order_by(Users.firstName.asc())
         # print(users)
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
@app.route("/admin/userInsert", methods = ["POST"]) #'admin/userInsert points to the URL for the form in html file'
def user_insert():
    print("here adding")
    print("Type: ", request.form.get('accessType'))
    if request.form.get('accessType') == "program_chair":
        add_program_chair(request)
    elif request.form.get('accessType') == 'division_chair':
        add_division_chair(request)
    elif request.form.get('accessType') == 'administrator' :
        # user = Users.get(username = request.form.get("userToAdd"))
        # user.isAdmin = 1
        # user.save () # We add save() for admin because it is not adding a new record
        # flash("Administrator successfully changed")
        add_administrator(request)
    return redirect(url_for("userManagement"))


    #for updating removed users
    # elif request.form.get('removeuser') == 'removeuser':
    #     if request.form.get('access') == "program_chair":
    #         # programchair = Users.get(Users.username == request.form.get("userToRemove"), Users.PID == request.form.get("program"))
    #         # programchair.delete_instance()
    #         # flash("Your changes have been successfully saved!")
    #         currentChair = Users.select().where(Users.PID == program)
    #         newChairs   = request.form.get("userToRemove")
    #         if currentChair.username not in newChairs:
    #             message = "USER: {0} has been removed as a program chair for pid: {1}".format(currentChair.username ,pid)
    #             log.writer("INFO", page, message)
    #             currentChair.PID = None
    #             currentChair.save()
    #         else:
    #         #HOWEVER IF THEY ARE PART OF THE LIST, DELETE THEM FROM THE LIST
    #             newChairs.remove(currentChair.username)
    #
    #     elif request.form.get('access') == 'division_chair':
    #         divisionchair = Users.get(Users.username == request.form.get("userToRemove"), Users.DID== request.form.get("division"))
    #         dc.delete_instance()
    #         flash("Your changes have been successfully saved!")
    #     elif request.form.get('access') == 'administrator' :
    #         user = Users.get(Users.username == request.form.get("userToRemove"))
    #         user.isAdmin = 0
    #         user.save()


def add_program_chair(request):
    print("here2")
    # programchair = Users.get_or_create(username = request.form.get("userToAdd"), PID =request.form.get("program"))
    # flash("Your changes have been successfully saved!")
    newChairs   = request.form.get("userToAdd")
    print(newChairs)
    PID =request.form.get("program")
        # for user_name in newChairs:
          #ADD THE USERNAMES TO THE PROGRAM CHAIR LIST
    newChair  = Users.get(Users.username == newChairs)
    print (newChair.username)
    newChair.PID = PID
    newChair.save()
    message = "USER: {0} has been added as a program chair for pid: {1}".format(newChairs,PID)
    app.logger.info(message)
    flash("Program successfully changed")

def add_division_chair(request):
    newChairs    = request.form.get("userToAdd")
    DID          = request.form.get("division")
    newChair     = Users.get(Users.username == newChairs)
    newChair.DID = DID
    newChair.save()
    message      = "USER: {0} has been added as a division chair for did: {1}".format(newChairs,DID)
    app.logger.info(message)
    flash("Division successfully changed")

@app.route("/admin/userManagement/get_admin", methods = ["GET"])
def administrators():
    alladmin = Users.select().where(Users.isAdmin == 1)
    newadmin={}
    print(alladmin)
    for admin in alladmin:
        newadmin[admin.username]={'firstname':admin.firstName,
                        'lastname':admin.lastName,
                        'username':admin.username
        }
    return json.dumps(newadmin)

@app.route('/admin/userManagement/get_program_chairs/<program>', methods = ["GET"])
def program_chair(program):
    allchairs = Users.select().where(Users.PID==program)
    print(allchairs, "hello")
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
