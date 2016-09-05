[TOC]
#Installation#
##Requirements##
* python 2.7
* linux, unix, mac, windows(with attachments)
* git

## Creating Development Environment 

1. ** Fork ** the repository from BitBucket and rename the project 

2. If working on a **local machine**, then clone the repo from your terminal. 

3. If you are working from cloud 9 follow [these steps](https://codymyers93.wordpress.com/2016/03/07/octoprint-working-in-cloud-9/) for directions on how to setup cloud 9 with git.

4. After you have successfully clone the repo. Run:
``` bash
source setup.sh
python app.py
```

If you are successful you will see something like:
``` bash
Starting application
Running server at http://0.0.0.0:8080/ 
```
Click the link in your terminal to check if it deployed correctly.

# Working with the flask template #
- bcsr-flask
	- App
		-static
			- js
			- css
			- img
		-templates
			- snips # A directory for partial html files 
			- start.html #This is an example of where your html files will go
		-logic 
			- files that manipulate the database
		- __init__.py
		- allImports.py
		- config.yaml
		- models.py
		- starty.py #This an example of where your controllers will go
			
