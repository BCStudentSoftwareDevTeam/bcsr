from allImports import *

@app.route("/archive", methods = ["GET"])

def archive():
    return render_template("archive.html",
                            cfg = cfg
                            )