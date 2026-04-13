from app.allImports import *
#IMPORT LOGIC FILES
from app.logic import databaseInterface
from app.logic.getAuthUser import AuthorizedUser
from app.logic.getCourses import GetCourses
from app.logic.switch import switch
from app.logic.getAll import GetAll

from app.models import Courses, Semesters, UsersCourses, Users
from flask import request, render_template

@app.route("/courses", methods = ["GET"]) #SET A DEFAULT APP ROUTE
@app.route("/courses/<term>", methods = ["GET"]) #SET A DEFAULT APP ROUTE
def courses(term = 0):
  if term == 0:
    # Gets the highest term id (201711, 201712, etc)
    currentSEID = databaseInterface.grab_current_semester()
  else:
    # Uses the term passed in via URL
    currentSEID = term
  current_term = Semesters.get(Semesters.SEID == currentSEID)
  #instantiate GetAll object
  getAll = GetAll()

  #Grab user information
  auth       = AuthorizedUser()
  user       = auth.get_user()
  user_level = auth.user_level()
  #CREATE TWO DEFAULT DICTIONARIES


  getCourses            = GetCourses(auth)

  # we need to get the dictionaries that populate the tables
  two_dictionaries      = getAll.create_dictionaries(currentSEID)
  divisions_to_programs = two_dictionaries[0]
  programs_to_courses   = two_dictionaries[1]
  # MY COURSES SELECT QUERY
  my_courses                  = getCourses.check_for_my_courses(currentSEID)
  # RENDER CORRECT PAGE BASED ON ACCESS LEVEL
  for case in switch(user_level):
    if case('admin'):
      return render_template('courses/admin.html',
                              cfg                   = cfg,
                              my_courses            = my_courses,
                              isAdmin               = auth.isAdmin,
                              divisions_to_programs = divisions_to_programs,
                              programs_to_courses   = programs_to_courses,
                              current_term          = current_term
                             )
      break;
    if case('division'):
      division_key            = user.DID
      # print division_key
      return render_template('courses/division.html',
                              cfg                   = cfg,
                              my_courses            = my_courses,
                              division_key          = division_key,
                              divisions_to_programs = divisions_to_programs,
                              programs_to_courses   = programs_to_courses,
                              current_term          = current_term
                             )
      break;
    if case('program'):
      program_key             = user.PID.name
      return render_template('courses/program.html',
                              cfg                   = cfg,
                              my_courses            = my_courses,
                              program_key           = program_key,
                              programs_to_courses   = programs_to_courses,
                              current_term          = current_term
                             )
      break;

    if case('faculty'):
      return render_template('courses/faculty.html',
                              cfg                   = cfg,
                              my_courses            = my_courses,
                              current_term          = current_term
                             )
      break;
    if case():
      # TODO: return ERROR
      abort(404)
      render_template('error.html')

@app.route("/course-search", methods=["GET"])
def course_search():

  prefix  = request.args.get("prefix", "").strip()
  number  = request.args.get("number", "").strip()
  results = None
  if not prefix and not number:
      flash("Please enter a course prefix and number (e.g. CSC 226).")
  elif prefix or number:
      if not prefix:
          flash("Please enter a course prefix (e.g. CSC).")
      elif not number:
          flash("Please enter a course number (e.g. 226).")
      else:
          results = (UsersCourses
                      .select(UsersCourses, Courses, Semesters, Users)
                      .join(Courses)
                      .join(Semesters)
                      .switch(UsersCourses)
                      .join(Users)
                      .where(
                          (Courses.prefix == prefix) &
                          (Courses.number == number)
                      )
                      .order_by(Semesters.SEID.desc()))
          
  return render_template("search.html", results=results, cfg=cfg)