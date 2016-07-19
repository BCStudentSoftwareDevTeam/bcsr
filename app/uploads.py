from allImports import *
import os
import datetime
#IMPORT LOGIC FILES
from app.logic.getAuthUser import AuthorizedUser 
@app.route('/uploads/<CID>', methods=['POST'])
def uploads(CID):
  auth       = AuthorizedUser()
  user_name  = auth.get_username()
  app.logger.info("{0} attempting to upload file.".format(user_name))
  file = request.files['file']
  app.logger.info("filename: {0}".format(file.filename))
  try:
    #RETRIEVE THE COURSE INFORMATION FROM THE post_CID
    course_info         = (Courses
                                .select()
                                .join(Programs)
                                .join(Divisions)
                                .where(
                                        Courses.CID  == CID,
                                        Courses.PID  == Programs.PID,
                                        Programs.DID == Divisions.DID
                                      )).get()

    #SET THE FILE PATH FOR THE UPLOAD FOLDER
    upload_file_path       = 'app/' + cfg['fileOperations']['dataPaths']['uploads'] #We need the app in the front in order to mkdir
    app.logger.info("uploads path: {0}".format(cfg['fileOperations']['dataPaths']['uploads']))
    course_file_path       = (    "/" 
                                +  str(course_info.SEID.SEID) 
                                + "/" 
                                + str(course_info.PID.DID.name) 
                                + "/" 
                                + str(course_info.prefix) 
                                + "/"
                              ).replace(" ","")
    directory_paths = upload_file_path+course_file_path
    #CHECK TO SEE IF THE PATH EXSIST IF NOT CREATE IT
    
    if not os.path.exists(directory_paths):
      try:
        app.logger.info("Trying to make directories")
        os.makedirs(directory_paths)
      except OSError as e:
        print e.errno
        pass
    new_file_name          = (    'CID' 
                                + str(course_info.CID) 
                                + '-' 
                                + str(course_info.prefix) 
                                +  '-' 
                                + str(course_info.number) 
                                + '-' 
                                + str(course_info.PID.DID.name) 
                                + '-' 
                                + user_name
                                + "." 
                                + str(file.filename.split(".").pop())
                              ).replace(" ","")
                              
    complete_path          = (   directory_paths
                                + new_file_name
                              ).replace(" ", "")
                              
    file.save(complete_path)
    database_path = course_file_path+new_file_name
    update_course_path = Courses.update(filePath=database_path).where(Courses.CID==CID)
    update_course_path.execute()
    get_time = datetime.datetime.now()
    time_stamp = get_time.strftime("%Y-%m-%d %H:%M")
    last_modified_message = "Uploaded By {0} On {1}".format(user_name,str(time_stamp))
    update_last_modified  = Courses.update(lastModified=last_modified_message).where(Courses.CID==CID)
    update_last_modified.execute()
    return redirect(url_for("courses"))
  except Exception as e:
    app.logger.info("{0}".format(e))
    return render_template("error.html",
                          cfg                   = cfg,
                          message               = "An error occured during the upload process."
                        )

  