from allImports import *
from app.logic.getAuthUser import AuthorizedUser


@app.route("/admin/programManagement/<pid>", methods=["GET", "POST"])
def adminProgramManagement(pid):
    # if (request.method == "GET"):
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin:
      users = Users.select()
      divisions = Divisions.select()
      programs  = Programs.select()
      program = Programs.get(Programs.PID == pid)
      programChairs = {}
      programChairs[program.PID] = Users.select().where(Users.PID == pid)
      for chair in programChairs[program.PID]:
          print chair.username
      return render_template("/admin/editProgram.html",
                              program       = program,
                              programChairs = programChairs,
                              cfg           = cfg,
                              users         = users,
                              divisions     = divisions,
                              programs      = programs,
                              isAdmin       = authorizedUser.isAdmin)
    #TODO: We should add an else statement that sends them to 404 
    #sending to 403 instead
    else:
        abort(403)
   