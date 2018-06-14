from allImports import *
from app.logic import databaseInterface 
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url

#Add Course
@app.route('/admin/courseManagement/addCourse',methods=["GET","POST"])
def addCourse():
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin:
        if request.method == "GET":
            semesters = Semesters.select()
            programs  = Programs.select()
            users     = Users.select()
            return render_template('admin/courseManagement/addCourse.html',
                                   cfg        = cfg,
                                   isAdmin    = authorizedUser.isAdmin,
                                   semesters  = semesters,
                                   programs   = programs,
                                   users      = users)
        elif request.method == "POST":
            data = request.form
            try:
                new_course = databaseInterface.insert_course(str(data['prefix']).upper(),
                                                        str(data['number']),
                                                        str(data['section']).upper(),
                                                        int(data['PID']),
                                                        int(data['SEID'])
                                                    )
                if new_course:
                    new_user_course = databaseInterface.insert_course_user(str(data['user']),int(new_course.CID))
                    if new_user_course:
                        flash('The course ({0} {1}) has been added'.format(data['prefix'],data['number']))
                    else:
                        flash('Course failed to be uploaded with instructor. Contact the system support')
                else:
                    flash('There was an error adding the course. The course was not added.')
            except Exception as e:
                flash(e)
            return redirect(url_for("addCourse"))
        else:
            abort(404)
    else:
        abort(403)
        
