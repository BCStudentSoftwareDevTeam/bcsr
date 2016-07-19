from allImports import *
import datetime
#IMPORT LOGIC FILES
from app.logic.getAuthUser import AuthorizedUser 
from app.logic import databaseInterface

@app.route("/delete/<CID>", methods = ["POST"])
def delete(CID):
  auth      = AuthorizedUser()
  user_name = auth.get_username()
  try:
    #need to add app/ in the front to tell the os where to start looking
    file_path = 'app/'+databaseInterface.get_course_file_path(CID)
    #Remove file from server
    os.remove(file_path)
    #Remove the file from the database
    delete_filePath = Courses.update(filePath=None).where(Courses.CID==CID)
    delete_filePath.execute()
    #RECORD THE CHANGE
    get_time = datetime.datetime.now()
    time_stamp = get_time.strftime("%Y-%m-%d %H:%M")
    last_modified_message = "Deleted By {} On {}".format(user_name,str(time_stamp))
    update_last_modified  = Courses.update(lastModified=last_modified_message).where(Courses.CID==CID)
    update_last_modified.execute()
    return redirect(url_for('courses'))
    
  except Exception,e:
    app.logger.info("{0} attempting to delete a syllabus.".format(str(e)))
    message = "An error occured during the delete process of the file."
    return render_template("error.html",
                              cfg                   = cfg,
                              message               = message
                            )