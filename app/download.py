#from Python
import os
import sys
import zipfile
#from Flask
from allImports import *
from flask import send_file
from flask import send_from_directory
# From Logic 
from app.logic.redirectBack import redirect_url
from app.logic import databaseInterface
from app.logic.getAuthUser import AuthorizedUser



@app.route("/download/<CID>", methods = ["POST"])
def download(CID):
  try:
    file_path = databaseInterface.get_course_file_path(CID)
    return send_file(file_path, as_attachment=True)
  
  except Exception,e:
    app.logger.info("{0} attempting to upload file.".format(str(e)))
    message = "An error occured during the download process."
    return render_template("error.html",
                              cfg                   = cfg,
                              message               = message
                            )
                            
@app.route("/admin/download/SEID/<SEID>", methods=["POST","GET"])
def downloadAll(SEID):
  authorizedUser = AuthorizedUser()
  if authorizedUser.isAdmin:
    #For os stuff we need to include app because it doesn't know to start at
    #app like in flask
    parent_folder   = 'app/' + cfg['fileOperations']['dataPaths']['uploads']
    zip_path        = cfg['fileOperations']['dataPaths']['zips'] + '/' + SEID + '.zip'
    output_path     = 'app/' + zip_path
    try:
      contents      = os.walk(parent_folder)
      zip_file      = zipfile.ZipFile(output_path,"w",zipfile.ZIP_DEFLATED)
      for root, folders, files in contents:
        for folder_name in folders:
          absolute_path = os.path.join(root, folder_name)
          relative_path = absolute_path.replace(parent_folder + '\\', '')
          print "Adding '%s' to Archive" % absolute_path
          zip_file.write(absolute_path, relative_path)
        for file_name in files:
          absolute_path = os.path.join(root, file_name)
          relative_path = absolute_path.replace(parent_folder +'\\', '')
          
          print "Adding '%s' to Archive" % output_path
          zip_file.write(absolute_path, relative_path)
          print "'%s' created successfully." % output_path
      zip_file.close()
      return send_file(zip_path,as_attachment=True)
      
    except Exception,e:
      return render_template('error.html',
                              cfg = cfg,
                              message = e
                              )
  
      
      

