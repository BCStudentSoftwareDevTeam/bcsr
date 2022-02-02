## Built With

* [Flask](http://flask.pocoo.org/docs/0.11/)  - Python Based Web Framework Used
* [Jinja2](http://jinja.pocoo.org/docs/dev/) - HTML Templating Language for Python
* [Peewee](http://docs.peewee-orm.com/en/latest/index.html) - A small, expressive ORM used for database communications
* [SQLite](https://sqlite.org/) - SQL database engine

# BCSR Application Installation

##Requirements##
* python 2.7
* linux, unix, mac, windows(with attachments)
* git

## Creating Development Environment

1. Clone the BCSR repository (from Github) in your home directory: ```git clone <URL>```

2. If working on a **local machine**, then clone the repo from your terminal.

3. Run ```source setup.sh```

## Creating the database

1. 

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
