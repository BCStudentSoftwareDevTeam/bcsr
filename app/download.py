#from Python
import os
from os.path import basename
import sys
import zipfile
#from Flask
from app.allImports import *
from flask import send_file
from flask import send_from_directory
# From Logic
from app.logic.redirectBack import redirect_url
from app.logic import databaseInterface
from app.logic.getAuthUser import AuthorizedUser



@app.route("/download/<CID>", methods = ["GET"])
def download(CID):
    page = r"/" + request.url.split("/")[-1]
    try:
        file_path = databaseInterface.get_course_download_file_path(CID)        
        message = "Download: {} has been downloaded".format(file_path)
        log.writer("INFO", page, message)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        app.logger.info("{0} attempting to download file.".format(str(e)))
        message = "An error occured during the download process."
        return render_template("error.html",
                                  cfg                   = cfg,
                                  message               = message
                                )

@app.route("/admin/download/SEID/<SEID>", methods=["POST","GET"])
def downloadAll(SEID):
    page = r"/" + request.url.split("/")[-1]
    authorizedUser = AuthorizedUser()
    # we need the location so that we can use relative file paths
    here = os.path.dirname(__file__)
    if authorizedUser.isAdmin:
        #For os methods we need to include app because it doesn't know to start at
        #app like in flask
        parent_folder   = cfg['fileOperations']['dataPaths']['download'] + '/' + SEID
        # get full path
        parent_folder   = os.path.join(here, parent_folder)
        zip_path        = cfg['fileOperations']['dataPaths']['zips'] + '/' + SEID + '.zip'
        zip_path        = os.path.join(here, zip_path)
        try:
          contents      = os.walk(parent_folder)
          zip_file      = zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED)
          for root, folders, files in contents:
              for folder_name in folders:
                  absolute_path = os.path.join(root, folder_name)
                  relative_path = absolute_path.replace(parent_folder, '')
                  zip_file.write(absolute_path, relative_path)
              for file_name in files:
                  absolute_path = os.path.join(root, file_name)
                  relative_path = absolute_path.replace(parent_folder, '')
                  zip_file.write(absolute_path, relative_path)
          zip_file.close()
          message = 'Download: {0} has been downloaded as a zip'.format(parent_folder)
          log.writer("INFO", page, message)
          return send_file(zip_path,as_attachment=True)
        except Exception as e:
            return render_template('error.html',
                              cfg = cfg,
                              message = e
                              )
    else:
        abort(403)
