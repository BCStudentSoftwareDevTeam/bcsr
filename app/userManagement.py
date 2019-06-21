from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.getSemesterManagement import GetSemesterManagement
from app.logic import databaseInterface

@app.route("/admin/userManagement", methods=["GET", "POST"])
def userManagement():
  page = "/" + request.url.split("/")[-1] #We need page for logging purposes
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:              #Ensure that the user is an Admin
    #Class from logic folder
    semester    = GetSemesterManagement()
    programs  = Programs.select()
    # program = Programs.get(Programs.PID) Scott said we probably dont need this
    programChairs[program.PID] = Users.select().where(Users.PID == pid)
    #DatabaseInterface from logic folder
    semesters = databaseInterface.get_all_semesters()
    users     = databaseInterface.get_non_admins()
    admins    = databaseInterface.get_all_admins()
    return render_template('admin/userManagement.html',
                            cfg = cfg,
                            #This variable is for the navbar
                            isAdmin   = authorizedUser.isAdmin,
                            programChairs = programChairs,
                            users     = users,
                            admins    = admins,
                            program   = program,
                            programs  = programs
                            )
  else:
    abort(403)


# This is for division
@app.route("/admin/userManagement/<did>", methods=["GET", "POST"])
def adminDivisionManagement(did):
  if (request.method == "GET"):
      authorizedUser = AuthorizedUser()
      # only admin should be able to change division chairs
      if authorizedUser.isAdmin:
         # every user could be division chair
         users = Users.select()
         #sidebar element
         divisions = Divisions.select()

         #division we are viewing
         division = Divisions.get(Divisions.DID == did)
         # organize all the division chairs
         divisionChairs = {}
         divisionChairs[division.DID] = Users.select().where(Users.DID == did)

         return render_template("/admin/userManagement.html",
                                 division      = division,
                                 divisionChairs = divisionChairs,
                                 cfg           = cfg,
                                 users         = users,
                                 divisions     = divisions,
                                 isAdmin       = authorizedUser.isAdmin)
      else:
         abort(403)


# This is for programs
@app.route("/admin/userManagement/<pid>", methods=["GET", "POST"])
def adminProgramManagement(pid):
    # if (request.method == "GET"):
    authorizedUser = AuthorizedUser()

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
      return render_template("/admin/userManagement.html",
                              program       = program,
                              programChairs = programChairs,
                              cfg           = cfg,
                              users         = users,
                              divisions     = divisions,
                              programs      = programs,
                              isAdmin       = authorizedUser.isAdmin)
    #sending to 403 instead
    else:
        abort(403)
