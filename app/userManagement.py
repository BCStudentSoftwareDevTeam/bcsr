from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from flask import json, jsonify
from app.logic import databaseInterface

@app.route("/admin/userManagement", methods=["GET"])
def adminDivisionManagement():
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

    if request.form.get('access') == "program_chair":
        pch = ProgramChair.get_or_create(username = request.form.get("userToAdd"), pid =request.form.get("program"))
        flash("Your changes have been successfully saved!")
    elif request.form.get('access') == 'division_chair':
        dc = DivisionChair.get_or_create(username = request.form.get("userToAdd"), did = request.form.get("division"))
        flash("Your changes have been successfully saved!")
    elif request.form.get('access') == 'administrator' :
        user = Users.get(username = request.form.get("userToAdd"))
        user.isAdmin = 1
        user.save() # We add save() for admin because it is not adding a new record


    #for updating removed users
    elif request.form.get('removeuser') == 'removeuser':
        if request.form.get('access') == "program_chair":
            pc = ProgramChair.get(ProgramChair.username == request.form.get("userToRemove"), ProgramChair.pid == request.form.get("program"))
            pc.delete_instance()
            flash("Your changes have been successfully saved!")
        elif request.form.get('access') == 'division_chair':
            dc = DivisionChair.get(DivisionChair.username == request.form.get("userToRemove"), DivisionChair.did== request.form.get("division"))
            dc.delete_instance()
            flash("Your changes have been successfully saved!")
        elif request.form.get('access') == 'administrator' :
            user = Users.get(Users.username == request.form.get("userToRemove"))
            user.isAdmin = 0
            user.save()

    return redirect(url_for("userManagement"))


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
