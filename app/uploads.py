from app.allImports import *
import os
import datetime
from hmac import compare_digest
from flask import session
from werkzeug.exceptions import HTTPException
#IMPORT LOGIC FILES
from app.logic.getAuthUser import AuthorizedUser
from app.logic.getUploads import GetUploads
from app.logic import databaseInterface
from app.models import *


@app.route('/uploads/<CID>', methods=['POST'])
def uploads(CID):
    auth = AuthorizedUser()
    user_name = auth.get_username()
    token = session.get('syllabus_upload_token')
    submitted_token = request.form.get('uploadToken', '')
    if (session.get('syllabus_upload_user') != user_name or not token or
            not compare_digest(token.encode('utf-8'), submitted_token.encode('utf-8'))):
        abort(403)

    file = request.files.get('file')
    if file is None or not file.filename:
        abort(400)

    try:
        # Lock the course until the file and metadata are saved. A repeated
        # submission must not overwrite a syllabus, even from another tab.
        with mainDB.atomic():
            course = (Courses.select().where(Courses.CID == CID)
                      .for_update().get_or_none())
            if course is None:
                abort(404)

            user = auth.get_user()
            is_instructor = UsersCourses.select().where(
                (UsersCourses.username == user_name) &
                (UsersCourses.CID == CID)).exists()
            manages_program = (user.PID_id is not None and
                               user.PID_id == course.PID_id)
            manages_division = (user.DID_id is not None and
                                user.DID_id == course.PID.DID_id)
            if not (auth.isAdmin or is_instructor or manages_program or manages_division):
                abort(403)
            if course.filePath is not None:
                abort(409, description="This course already has a syllabus. Refresh the courses page.")

            getUploads = GetUploads(file)
            upload_path = getUploads.get_upload_path()
            course_path = getUploads.get_course_path(CID)
            directory_path = upload_path + course_path
            getUploads.check_path_exist(directory_path)
            instructors_string = databaseInterface.get_course_instructors(CID)
            new_file_name = getUploads.create_filename(CID, instructors_string)
            complete_path = (directory_path + new_file_name).replace(" ", "")
            file.save(complete_path)
            if not os.path.exists(complete_path):
                raise OSError("The syllabus file was not saved.")

            database_path = (course_path + new_file_name).replace(" ", "")
            time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M")
            last_modified_message = "Uploaded By {0} On {1}".format(user_name, time_stamp)
            Courses.update(filePath=database_path,
                           lastModified=last_modified_message).where(Courses.CID == CID).execute()

        message = "Uploads: {0} has been {1}".format(new_file_name, last_modified_message)
        log.writer("INFO", "/uploads/{0}".format(CID), message)
        # A refresh after a normal form submission must repeat only the GET.
        return redirect(url_for("courses"), code=303)
    except HTTPException:
        raise
    except Exception as e:
        app.logger.error("{0}".format(e))
        return render_template("error.html", cfg=cfg,
                               message="An error occured during the upload process."), 500
