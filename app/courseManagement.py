from allImports import *
from app.logic import databaseInterface 
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.excelMaker import makeExcelFile
from flask import send_file

''' 
Variable: activePage
Purpose: This variable is used to control what should be inside of the 
page-wrapper for section for courseManagement. This variable should be the file
path to an html file located inside of admin/courseManagementSnips.

Example:
    activePage = "admin/courseManagementSnips/missingSyllabi.html'''

#Missing Syllabi
@app.route("/admin/courseManagement/missingSyllabi", methods=["GET","POST"])
def missingSyllabi():
    authorizedUser = AuthorizedUser()
    activePage = "admin/courseManagementSnips/missingSyllabi.html"
    if authorizedUser.isAdmin:
        if request.method == "GET":
            semesters = Semesters.select()
            return render_template('admin/courseManagement.html',
                                cfg           = cfg,
                                isAdmin       = authorizedUser.isAdmin,
                                activePage    = activePage,
                                semesters     = semesters)
        elif request.method == "POST":
            try:
                data = request.form
                filePath = makeExcelFile(data['SEID'])
                return send_file(filePath,as_attachment=True)
            except Exception as e:
                #TODO: Log e
                print e
                flash('Error occured while trying to prepare excel sheet. ')
                return redirect(url_for("missingSyllabi"))
        else:
            abort(404)
    else:
        abort(403)
        
#Add Course
@app.route('/admin/courseManagement/addCourse',methods=["GET","POST"])
def addCourse():
    authorizedUser = AuthorizedUser()
    activePage = "admin/courseManagementSnips/addCourse.html"
    if authorizedUser.isAdmin:
        if request.method == "GET":
            prefixes  = Courses.select(Courses.prefix).distinct()
            semesters = Semesters.select()
            programs  = Programs.select()
            users     = Users.select()
            return render_template('admin/courseManagement.html',
                                   cfg        = cfg,
                                   isAdmin    = authorizedUser.isAdmin,
                                   activePage = activePage,
                                   prefixes   = prefixes,
                                   semesters  = semesters,
                                   programs   = programs,
                                   users      = users)
        elif request.method == "POST":
            data = request.form
            try:
                new_course = databaseInterface.insert_course(str(data['prefix']),
                                                        str(data['number']),
                                                        str(data['section']),
                                                        int(data['PID']),
                                                        int(data['SEID'])
                                                    )
                if new_course:
                    new_user_course = databaseInterface.insert_course_user(str(data['user']),int(new_course.CID))
                    if new_user_course:
                        flash('The course ({0} {1}) has been added'.format(data['prefix'],data['number']))
                    else:
                        flash('Course failed to be uploaded with instructor. Contact customer support')
                else:
                    flash('There was an error adding the course. The course was not added.')
            except Exception as e:
                flash(e)
            return redirect(url_for("addCourse"))
        else:
            abort(404)
    else:
        abort(403)
                            