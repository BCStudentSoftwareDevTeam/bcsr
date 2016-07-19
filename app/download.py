from allImports import *
from flask import send_file

@app.route("/download/<CID>", methods = ["POST","GET"])
def download(CID):
  try:
    course_path = (Courses
                    .select(Courses.filePath)
                    .where(
                            Courses.CID == CID
                          )
                  ).get()
    file_path = str(cfg['fileOperations']['dataPaths']['uploads']) + str(course_path.filePath)
    return send_file(file_path, as_attachment=True)
  
  except Exception,e:
    app.logger.info("{0} attempting to upload file.".format(str(e)))
    message = "An error occured during the download process."
    return render_template("error.html",
                              cfg                   = cfg,
                              message               = message
                            )
