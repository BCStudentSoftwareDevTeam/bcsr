from allImports import *
import datetime
#IMPORT LOGIC FILES
from app.logic.getAuthUser import AuthorizedUser 
from app.logic import databaseInterface
from app.logic.redirectBack import redirect_url

@app.route("/delete/<CID>", methods = ["POST"])
def delete(CID):
  page = r"/" + request.url.split("/")[-1]
  auth      = AuthorizedUser()
  user_name = auth.get_username()
  # if auth.user_level() == 'admin':
  try:
    #need to add app/ in the front to tell the os where to start looking
    file_path = 'app/'+databaseInterface.get_course_file_path(CID)
    #Remove file from server
    os.remove(file_path)
    #Remove the file from the database
    delete_filePath = Courses.update(filePath=None).where(Courses.CID==CID)
    delete_filePath.execute()
    flash("Syllabus has been deleted")
    #RECORD THE CHANGE
    get_time = datetime.datetime.now()
    time_stamp = get_time.strftime("%Y-%m-%d %H:%M")
    last_modified_message = "Deleted By {} On {}".format(user_name,str(time_stamp))
    message = "Uploads: {0} has been {1}".format(file_path, last_modified_message)
    log.writer('INFO', page, message)
    update_last_modified  = Courses.update(lastModified=last_modified_message).where(Courses.CID==CID)
    update_last_modified.execute()
    return redirect(redirect_url())
    
  except Exception,e:
    app.logger.info("{0} attempting to delete a syllabus.".format(str(e)))
    message = "An error occured during the delete process of the file."
    return render_template("error.html",
                              cfg                   = cfg,
                              message               = message
                            )
  # else:
    # abort(403)