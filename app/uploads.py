from allImports import *
import os
import datetime
#IMPORT LOGIC FILES
from app.logic.getAuthUser import AuthorizedUser
from app.logic.getUploads import GetUploads
from app.logic import databaseInterface

@app.route('/uploads/<fileType>/<CID>', methods=['POST','GET'])
def uploads(fileType, CID):
  auth       = AuthorizedUser()
  user_name  = auth.get_username()
  file = request.files['file']
  getUploads  = GetUploads(file)
  try:
    upload_path     = getUploads.get_upload_path(fileType)
    # print ("Here is the upload path:" + upload_path)
    #course_path is the map of where the syllabus should be in the upload folder
    course_path     = getUploads.get_course_path(CID)
    directory_path  = upload_path + course_path
    #Make sure that the directories exist and creates it if it doesn't
    result = getUploads.check_path_exist(directory_path)
    #Now we rename the file to our create standard
    instructors_string = databaseInterface.get_course_instructors(CID)
    if fileType == "syllabus":
      new_file_name   = getUploads.create_filename(CID, instructors_string)
    elif fileType == "other":
      new_file_name = file.filename
    complete_path   = (directory_path + new_file_name).replace(" ","")
    #Save the File
    file.save(complete_path)
    	#Now we need to course_path with its new file name to the database
    if os.path.exists(complete_path):
      database_path = (course_path+new_file_name).replace(" ","")
      if fileType == "syllabus":
        update_course_path = Courses.update(filePath=database_path).where(Courses.CID==CID)
        update_course_path.execute()
      elif fileType == "other":
        update_optional_path = Courses.update(optionalFilepath=database_path).where(Courses.CID==CID)
        update_optional_path.execute()
        
    	#Now we need to log the changes
    	get_time = datetime.datetime.now()
    	time_stamp = get_time.strftime("%Y-%m-%d %I:%M")
    	last_modified_message = "Uploaded By {0} On {1}".format(user_name,str(time_stamp))
    	# log in our log file
    	message = "Uploads: {0} has been {1}".format(new_file_name, last_modified_message)
    	page = "/uploads/{0}".format(CID)
    	log.writer("INFO", page, message)
    	#update the database to inform the users who uploaded the file
    	update_last_modified  = Courses.update(lastModified=last_modified_message).where(Courses.CID==CID)
    	update_last_modified.execute()
    	return redirect(url_for("courses"))
    else:
 	return render_template("error.html",
                               cfg     = cfg,
                               message = "An error occured during the upload process.")  
  except Exception as e:
    app.logger.info("{0}".format(e))
    return render_template("error.html",
                          cfg                   = cfg,
                          message               = "An error occured during the upload process."
                        )
