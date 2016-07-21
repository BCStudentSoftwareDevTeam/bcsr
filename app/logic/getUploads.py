'''
Purpose Of File: To hold all of the functions for app.courses
'''
from app.allImports import *
from app.logic import databaseInterface  

class GetUploads():
  def __init__(self, file):
    self.file   = file
  
  def get_upload_path(self):
    #We need the app in the front in order to mkdir
    upload_file_path = 'app/' + cfg['fileOperations']['dataPaths']['uploads']
    return upload_file_path

  def get_course_path(self,CID):
    course_info = databaseInterface.get_course_info(CID)
    course_file_path       = (  "/" 
                                +  str(course_info.SEID.SEID) 
                                + "/" 
                                + str(course_info.PID.DID.name) 
                                + "/" 
                                + str(course_info.prefix) 
                                + "/"
                              ).replace(" ","")
    return course_file_path
    
  def check_path_exist(self,path):
    if not os.path.exists(path):
        try:
          app.logger.info("Trying to make directories")
          os.makedirs(path)
        except OSError as e:
          print e.errno
          pass
    return 0
    
  def create_filename(self,CID, user_name):
    course_info = databaseInterface.get_course_info(CID)
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
                                + str(self.file.filename.split(".").pop())
                              ).replace(" ","")
    return new_file_name
  
        
    
         
    
        
    
        
    