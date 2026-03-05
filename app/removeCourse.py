from flask import json, jsonify

from app.allImports import *
from app.logic import databaseInterface
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.models import *

def SEID_courses_dict():
  dictionary = dict()
  terms = Semesters.select()
  for term in terms:
    courses  = Courses.select().where(Courses.SEID==term.SEID)
    SEID = str(term.SEID)
    dictionary[SEID] = courses
  return dictionary

@app.route('/admin/courseManagement/removeCourse',methods=["GET","POST"])
def removeCourse():
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:
    if request.method == "GET":
      semesters = Semesters.select()
      return render_template('admin/courseManagement/removeCourse.html',
                             cfg        = cfg,
                             isAdmin    = authorizedUser.isAdmin,
                             semesters  = semesters
                             )
    elif request.method == "POST":
      try:
        data = request.form
        course = Courses.get(Courses.CID == data['CID'])
        msg = 'The course (' + course.prefix + '-' + course.number + '-' + course.section + ') has been deleted.'
        UsersCourses.delete().where(UsersCourses.CID == data['CID']).execute()  # Delete any relationships to users as well
        Courses.delete().where(Courses.CID == data['CID']).execute()
        flash(msg)
        return redirect(url_for("removeCourse"))
      except Exception as e:
        flash(e)
        return redirect(url_for("removeCourse"))
    else:
      abort(404)
  else:
    abort(403)


@app.route('/admin/courseManagement/removeCourse/json/<SEID>',methods=["GET"])
def getJson(SEID):
  try:
    courseList = []
    courses  = Courses.select().where(Courses.SEID==SEID)
    for course in courses:
      try:
        user = UsersCourses.get(UsersCourses.CID == course.CID)
      except Exception as e:
        intructor = "None"
      courseTitle = course.prefix + '-' + course.number + '-' + course.section
      instructor = "(" + user.username.username + ") " + user.username.firstName + ' ' + user.username.lastName
      courseDict = {
        'CID'   : course.CID,
        'title' : courseTitle,
        'instructor' : instructor
      }
      courseList.append(courseDict)
    jsonStr = json.dumps(courseList)
    return jsonify(Courses=jsonStr)
  except Exception as e:
    # print str(e)
    pass
