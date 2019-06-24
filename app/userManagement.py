from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.getSemesterManagement import GetSemesterManagement
from app.logic import databaseInterface
from app.programManagement import adminProgramManagement

@app.route("/admin/userManagement", methods=["GET", "POST"])
def userManagement_get():
  page = "/" + request.url.split("/")[-1] #We need page for logging purposes
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:              #Ensure that the user is an Admin
    if request.method == "GET":
        print("Hello")
        #Class from logic folder
        # semester    = GetSemesterManagement()
        divisions = Divisions.select()

        #DatabaseInterface from logic folder
        # semesters = databaseInterface.get_all_semesters()
        # users     = databaseInterface.get_non_admins()
        # admins    = databaseInterface.get_all_admins()

        #
        programs  = Programs.select()
        print("Hello2")
        # program = Programs.get(Programs.PID == pid)
        # programChairs = {}
        # programChairs[program.PID] = Users.select().where(Users.PID == pid)
        # programChairs.save()
        return render_template('admin/userManagement.html',
                                cfg = cfg,
                                #This variable is for the navbar
                                isAdmin   = authorizedUser.isAdmin,
                                # users     = users,
                                # admins    = admins,
                                programs  = programs,
                                divisions = divisions
                                # divisions = divisions,
                                # program       = program,
                                # programChairs = programChairs,
                                # data = data,
                                # pid = pid
                                )
    elif request.method == "POST":
        def adminProgramManagement():
            # if (request.method == "GET"):
            authorizedUser = AuthorizedUser()
            data        = request.form
            pid         = data['PID']
            print(pid)
            # only admin  should be able to change program chairs
            if authorizedUser.isAdmin:

              # all uses could be program chair
              users = Users.select()

              #sidebar elements
              divisions = Divisions.select()
              programs  = Programs.select()

              # program we are viewing
              program = Programs.get(Programs.PID == pid)

              programChairs = {}
              programChairs[program.PID] = Users.select().where(Users.PID == pid)
              programChairs.save()
              return render_template("admin/userManagement.html",
                                      program       = program,
                                      programChairs = programChairs,
                                      cfg           = cfg,
                                      users         = users,
                                      divisions     = divisions,
                                      programs      = programs,
                                      isAdmin       = authorizedUser.isAdmin)

    else:
        abort(404)
  else:
    abort(403)


# This is for division
# @app.route("/admin/userManagement/<did>", methods=["GET", "POST"])
# def adminDivisionManagement(did):
#   if (request.method == "GET"):
#       authorizedUser = AuthorizedUser()
#       # only admin should be able to change division chairs
#       if authorizedUser.isAdmin:
#          # every user could be division chair
#          users = Users.select()
#          #sidebar element
#          divisions = Divisions.select()
#
#          #division we are viewing
#          division = Divisions.get(Divisions.DID == did)
#          # organize all the division chairs
#          divisionChairs = {}
#          divisionChairs[division.DID] = Users.select().where(Users.DID == did)
#
#          return render_template("/admin/userManagement.html",
#                                  division      = division,
#                                  divisionChairs = divisionChairs,
#                                  cfg           = cfg,
#                                  users         = users,
#                                  divisions     = divisions,
#                                  isAdmin       = authorizedUser.isAdmin)
#       else:
#          abort(403)
