from allImports import *
from flask import send_file
from app.logic import databaseInterface

@app.route("/download/<CID>", methods = ["POST","GET"])
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
