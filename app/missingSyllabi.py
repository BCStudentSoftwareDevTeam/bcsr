from flask import send_file
import os

from app.allImports import *
from app.logic import databaseInterface
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.excelMaker import makeExcelFile
from app.models import Semesters

#Missing Syllabi
@app.route("/admin/courseManagement/missingSyllabi", methods=["GET","POST"])
def missingSyllabi():
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin:
        if request.method == "GET":
            semesters = Semesters.select()
            return render_template('admin/courseManagement/missingSyllabi.html',
                                cfg           = cfg,
                                isAdmin       = authorizedUser.isAdmin,
                                semesters     = semesters)
        elif request.method == "POST":
            try:
                data = request.form
                filePath = makeExcelFile(data['SEID'])
                return send_file(filePath,as_attachment=True)
            except Exception as e:
                #TODO: Log e
                print(e)
                flash('Error occured while trying to prepare excel sheet. ')
                return redirect(url_for("missingSyllabi"))
        else:
            abort(404)
    else:
        abort(403)
