from allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from flask import json, jsonify
from app.logic import databaseInterface

@app.route("/admin/userManagement/changeDivisionChair", methods=["GET"])
def adminDivisionManagement():
  if (request.method == "GET"):
      authorizedUser = AuthorizedUser()
      # only admin should be able to change division chairs
      if authorizedUser.isAdmin:
         users     = databaseInterface.get_non_admins()
         divisions = databaseInterface.grab_all_divisions()
         print("first route")
         return render_template("admin/userManagement/changeDivision.html",
                                 divisions      = divisions,
                                 cfg           = cfg,
                                 users         = users,
                                 isAdmin       = authorizedUser.isAdmin)
      else:
         abort(403)

@app.route('/admin/userManagement/changeDivisionChair/<did>',methods=["GET"])
def get_divisions_json(did):
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin:
        users     = databaseInterface.get_non_admins()
        divisions = databaseInterface.grab_all_divisions()
        chairs = Users.select().where(Users.DID == did)
        chairList = []
        for chair in chairs:
            chairList.append(chair.username)
        print(chairList)
        # return jsonify({did: chairList})
    return render_template("admin/userManagement/changeDivision.html",
                            cfg           = cfg,
                            chairs = chairs,
                            chairList = chairList,
                            divisions      = divisions,
                            users         = users,
                            isAdmin       = authorizedUser.isAdmin)
