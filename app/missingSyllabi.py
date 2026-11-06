from flask import send_file
import os
from urllib.parse import quote, urlencode

from app.allImports import *
from app.logic import databaseInterface
from app.logic.getAuthUser import AuthorizedUser
from app.logic.redirectBack import redirect_url
from app.logic.excelMaker import makeExcelFile
from app.models import Semesters, Courses, UsersCourses

#Missing Syllabi
@app.route("/admin/courseManagement/missingSyllabi", methods=["GET","POST"])
def missingSyllabi():
    authorizedUser = AuthorizedUser()
    if authorizedUser.isAdmin:
        if request.method == "GET":
            assignment_missing_syllabi = (
                UsersCourses.select().join(Courses).where(Courses.filePath >> None)
            )

            courses_by_email = {}
            for assignment in assignment_missing_syllabi:
                instructor = assignment.username
                course = assignment.CID
                email = (instructor.email or "").strip()
                if email:
                    course_name = f"{course.prefix} {course.number} {course.section}"
                    instructor_details = courses_by_email.setdefault(
                        email, {"names": set(), "courses": set()}
                    )
                    instructor_details["names"].add(
                        f"{instructor.firstName} {instructor.lastName}".strip()
                    )
                    instructor_details["courses"].add(course_name)

            email_link = None
            if courses_by_email:
                body_lines = [
                    "Hello,",
                    "",
                    "The following course(s) are missing a syllabus:",
                ]
                for instructor_details in courses_by_email.values():
                    names = ", ".join(sorted(instructor_details["names"]))
                    course_names = ", ".join(sorted(instructor_details["courses"]))
                    body_lines.append(f"- {names}: {course_names}")
                body_lines.extend(["", "Please upload the syllabus. Thank you!"])
                email_link = "mailto:?" + urlencode(
                    {
                        "bcc": ",".join(sorted(courses_by_email)),
                        "subject": "Missing syllabus reminder",
                        "body": "\n".join(body_lines),
                    },
                    quote_via=quote,
                )

            semesters = Semesters.select()
            return render_template('admin/courseManagement/missingSyllabi.html',
                                cfg           = cfg,
                                isAdmin       = authorizedUser.isAdmin,
                                semesters     = semesters,
                                email_link    = email_link)
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
