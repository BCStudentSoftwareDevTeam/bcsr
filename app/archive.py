from allImports import *

@app.route("/archive/", defaults={'post_SEID': None}, methods = ["GET", "POST"])
@app.route("/archive/<post_SEID>", methods = ["GET", "POST"])
def archive(post_SEID):
    #SET DEFAULTS
    semesters = Semesters.select()
    if post_SEID != None:
        #PUT RETRIEVAL INFORMATION IN HERE
        comment = 'above'
    return render_template("archive.html",
                            cfg = cfg,
                            semesters = semesters,
                            SEID      = post_SEID
                            )