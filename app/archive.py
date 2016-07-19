from allImports import *

@app.route("/archive/", defaults={'post_SEID': None}, methods = ["GET", "POST"])
@app.route("/archive/<post_SEID>", methods = ["GET", "POST"])
def archive(post_SEID):
    
    if post_SEID != None:
        
        # division_info = (Divisions.select()
        #                             .where(Divisions)
        #                     )
        return render_template("archive.html",
                            cfg = cfg,
                            semesters = semesters,
                            SEID      = post_SEID
                            )
    else:
        return render_template("archive.html",
                            cfg = cfg,
                            semesters = semesters,
                            SEID      = post_SEID
                            )
    