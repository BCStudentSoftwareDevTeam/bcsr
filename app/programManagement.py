from allImports import *
from app.logic.getAuthUser import AuthorizedUser


@app.route("/admin/programManagement/<pid>", methods=["GET", "POST"])
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
      return render_template("/admin/editProgram.html",
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
   