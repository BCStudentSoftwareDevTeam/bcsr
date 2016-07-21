from allImports import *
from app.logic.getAuthUser import AuthorizedUser


@app.route("/admin/divisionManagement/<did>", methods=["GET", "POST"])
def adminDivisionManagement(did):
  if (request.method == "GET"):
      authorizedUser = AuthorizedUser()
      if authorizedUser.isAdmin:
         users = Users.select()
         divisions = Divisions.select()
         division = Divisions.get(Divisions.DID == did)
         divisionChairs = {}
         divisionChairs[division.DID] = Users.select().where(Users.DID == did)
         
         return render_template("/admin/editDivision.html",
                                 division      = division,
                                 divisionChairs = divisionChairs,
                                 cfg           = cfg,
                                 users         = users,
                                 divisions     = divisions,
                                 isAdmin       = authorizedUser.isAdmin)