from allImports import *
from app.logic.getAuthUser import AuthorizedUser


@app.route("/admin/userManagement/changeDivisionChair", methods=["GET"])
def adminDivisionManagement():
  if (request.method == "GET"):
      authorizedUser = AuthorizedUser()
      # only admin should be able to change division chairs
      if authorizedUser.isAdmin:
         # every user could be division chair
         users = Users.select()
         #sidebar element
         division = Divisions.select()
         #division we are viewing
         # divisions = Divisions.get(Divisions.DID == did)
         # # organize all the division chairs
         # divisionChairs = {}
         # divisionChairs[division.DID] = Users.select().where(Users.DID == did)

         return render_template("admin/userManagement/changeDivision.html",
                                 # divisions      = divisions,
                                 # divisionChairs = divisionChairs,
                                 cfg           = cfg,
                                 users         = users,
                                 division     = division,
                                 isAdmin       = authorizedUser.isAdmin)
      else:
         abort(403)
