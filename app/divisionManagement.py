from app.allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.models import Users, Divisions

@app.route("/admin/divisionManagement/<did>", methods=["GET", "POST"])
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

         return render_template("/admin/editDivision.html",
                                 division      = division,
                                 divisionChairs = divisionChairs,
                                 cfg           = cfg,
                                 users         = users,
                                 divisions     = divisions,
                                 isAdmin       = authorizedUser.isAdmin)
      else:
         abort(403)
