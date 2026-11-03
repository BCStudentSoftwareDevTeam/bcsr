'''
Purpose Of File: The pages an admin goes through to create a term from a course
list spreadsheet: upload the file, review it, confirm, and see the results.
Nothing is written to the database until the admin confirms.
'''
import os
from flask import session

from app.allImports import *
from app.logic.getAuthUser import AuthorizedUser
from app.logic.getSemesterManagement import GetSemesterManagement
from app.logic import courseImport
from app.logic import databaseInterface

#The session only holds the token of the upload that is being reviewed
SESSION_KEY = "courseImportToken"

def get_pending():
  '''Purpose: Gets the upload the admin is working on, or None if there is
  not one or it has expired.'''
  token   = session.get(SESSION_KEY)
  pending = courseImport.load_pending(token)
  return token, pending

@app.route("/admin/semesterManagement/upload", methods=["POST"])
def uploadCourseList():
  page = "/" + request.url.split("/")[-1]
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:
    semester = GetSemesterManagement()
    term     = request.form.get('term', '')
    year     = request.form.get('year', '')
    file     = request.files.get('courseList')

    if not term.isdigit() or int(term) not in cfg['termInfo'] or year not in semester.get_years_list():
      flash("Choose a term and a year.", "danger")
      return redirect(url_for("semesterManagement"))
    if not file or file.filename == "":
      flash("Choose a course list file to upload.", "danger")
      return redirect(url_for("semesterManagement"))

    termName = cfg['termInfo'][int(term)]
    seid     = semester.create_seid({'year': year, 'term': term})
    if courseImport.semester_exists(seid):
      flash("Semester: {0} {1} already exists in the database.".format(termName, year), "danger")
      return redirect(url_for("semesterManagement"))

    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > cfg['courseImport']['allowedSize']['size']:
      flash("The file is too large. The limit is {0} MB.".format(cfg['courseImport']['allowedSize']['size'] // 1000000), "danger")
      return redirect(url_for("semesterManagement"))

    try:
      courses = courseImport.parse_course_file(file, file.filename)
    except courseImport.CourseImportError as e:
      log.writer("ERROR", page, "Course list rejected ({0}): {1}".format(file.filename, e))
      flash(str(e), "danger")
      return redirect(url_for("semesterManagement"))

    courseImport.validate_rows(courses, courseImport.get_prefix_map())
    #A new upload replaces the one that was being reviewed
    courseImport.discard_pending(session.get(SESSION_KEY))
    session[SESSION_KEY] = courseImport.save_pending({'stage':    'review',
                                                      'seid':     seid,
                                                      'term':     term,
                                                      'termName': termName,
                                                      'year':     year,
                                                      'filename': file.filename,
                                                      'courses':  courses})
    return redirect(url_for("confirmCourseUpload"))
  else:
    abort(403)

@app.route("/admin/semesterManagement/confirm", methods=["GET", "POST"])
def confirmCourseUpload():
  page = "/" + request.url.split("/")[-1]
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:
    token, pending = get_pending()
    if pending is None:
      flash("Your upload has expired. Please upload the course list again.", "danger")
      return redirect(url_for("semesterManagement"))
    if pending['stage'] != 'review':
      return redirect(url_for("courseImportResults"))

    summary = courseImport.summarize(pending['courses'])
    if request.method == "POST":
      if summary['importable'] == 0:
        flash("There are no courses that can be imported.", "danger")
        return redirect(url_for("confirmCourseUpload"))
      #Someone else may have created the term since the file was uploaded
      if courseImport.semester_exists(pending['seid']):
        flash("Semester: {0} {1} already exists in the database.".format(pending['termName'], pending['year']), "danger")
        return redirect(url_for("semesterManagement"))
      try:
        result = courseImport.import_term(pending['term'], pending['year'],
                                          pending['courses'], courseImport.get_prefix_map())
      except Exception as e:
        log.writer("ERROR", page, "Creating {0} {1} failed: {2}".format(pending['termName'], pending['year'], e))
        flash("An error occurred while creating {0} {1}. Nothing was saved.".format(pending['termName'], pending['year']), "danger")
        return redirect(url_for("confirmCourseUpload"))
      pending['courses'] = result['courses']
      pending['stage']   = 'imported'
      courseImport.save_pending(pending, token)
      #The same log entry and message the Add Semester route has always produced
      log.writer(result['logType'], page, result['message'])
      flash(result['message'])
      return redirect(url_for("courseImportResults"))

    return render_template('admin/confirmCourseUpload.html',
                            cfg           = cfg,
                            isAdmin       = authorizedUser.isAdmin,
                            pending       = pending,
                            summary       = summary,
                            #The most recent term automatically becomes the active term
                            becomesActive = int(pending['seid']) > databaseInterface.grab_current_semester(),
                            )
  else:
    abort(403)

@app.route("/admin/semesterManagement/results", methods=["GET"])
def courseImportResults():
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:
    token, pending = get_pending()
    if pending is None:
      return redirect(url_for("semesterManagement"))
    if pending['stage'] != 'imported':
      return redirect(url_for("confirmCourseUpload"))

    summary = courseImport.summarize(pending['courses'])
    summary['imported'] = summary['importable']
    issues  = [course for course in pending['courses'] if course['status'] != courseImport.OK]
    return render_template('admin/courseImportResults.html',
                            cfg     = cfg,
                            isAdmin = authorizedUser.isAdmin,
                            pending = pending,
                            summary = summary,
                            issues  = issues,
                            )
  else:
    abort(403)
