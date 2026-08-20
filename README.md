## Built With

* [Flask](http://flask.pocoo.org/docs/0.11/)  - Python Based Web Framework Used
* [Jinja2](http://jinja.pocoo.org/docs/dev/) - HTML Templating Language for Python
* [Peewee](http://docs.peewee-orm.com/en/latest/index.html) - A small, expressive ORM used for database communications
* [SQLite](https://sqlite.org/) - SQL database engine

# Setting Up a Linux Development Environment on Windows
### Getting Started With WSL ###

First check if WSL and Ubuntu are installed on your device by running these commands: ```wsl --status``` and (```wsl -l -v``` or ```wsl --list --verbose```) as administrator in Powershell. 

If WSL is not installed, in the same terminal run: ```wsl --install```. After it is completed run ```wsl -l -v``` to see if Ubuntu is installed.
If you don't see Ubuntu installed run: ```wsl --install -d Ubuntu```, then restart your laptop afterwards.

Then launch Ubuntu with: ```wsl``` then in a Ubuntu terminal you can run ```uname -a``` it will run Linux system info.

### Getting Your Development Environment Running

After you have set up WSL and Ubuntu, there are three additional steps that you will have to complete before your virtual environment will be completely operational. 

**Step One: Ensure you have MySQL installed**

First, check whether MySQL is already installed. From PowerShell, you can run: ```mysql --version ```. You can also check the MySQL installation directory: ```Get-ChildItem "C:\Program Files\MySQL" -ErrorAction SilentlyContinue ```. From WSL, you can check the Windows MySQL installation in bash with: ```ls "/mnt/c/Program Files/MySQL" ```.

If MySQL GUI is not installed: 
- Navigate to this website: https://dev.mysql.com/downloads/installer/ and download. You will see the prompt to log in or sign up instead choose “No thanks, just start my download.”
- During the installation process, you will be given the option to select client, server or both and you should choose both.

**Step Two: Activate Your Virtual Environment**

In order to do this, first you need to be in Ubuntu so run in your terminal: ```wsl```. 
Then all you have to do is type: ```source setup.sh``` into the Linux terminal. You might have to wait a minute or two as the tools you need for our application are downloaded into your virtual environment. However, after the setup is completed you should see the words ```(venv)``` at the front of your terminal.

- If you have this error: `-bash: setup.sh: line <something>: syntax error: unexpected end of file from "if" command on line 19` go to the bottom of your IDE and find CRLF and click it to select  LF

![venv.PNG](https://bitbucket.org/repo/bEXb4L/images/2846617267-venv.PNG) 

>***Note:*** 
In order for the application to work, you must activate the virtual environment. If you are not inside of the virtual environment you will see this error:
![venvError.PNG](https://bitbucket.org/repo/bEXb4L/images/1415469357-venvError.PNG)Whenever you get this error just activate the virtual environment again by entering the command ```source setup.sh```

>Also, If you ever want to deactivate the virtual environment for any reason just type ```deactivate``` into the terminal. 
![deactivate.PNG](https://bitbucket.org/repo/bEXb4L/images/2248015321-deactivate.PNG)

**Step Three: Setup Your Database**

A couple of elements are necessary in order to get your database established. The first step is creating the SQLite file, we can create the file in the desired location through the use of one of our scripts.

You would need to add this in config.yaml: 
```yaml
databases:
  dev: "data/bcsr.sqlite"
  stage: ""
  prod: "data/bcsr.sqlite"
```

Create the application's `data` directory if it does not already exist: ```mkdir -p data ``` Confirm that the directory exists: ```ls -la ```

**Create Database**

Enter into your mysql, either through the MySQL GUI or by typing ```mysql -u root -p```.

> **WARNING:** `create_db.py` is intended for development setup. Do not run this script against a production environment after real data exists.

Then, by typing the command ```python create_db.py``` a database file containing the correct schemas will be created in the data directory for development setup.

**How to View the Database** 

Now that you have the database created and populated with data, you are probably asking yourself how do I see that? Our system development team likes to use a tool called [DB Browser](http://sqlitebrowser.org/). This tool is a visual way of viewing and editing SQLite database files. 

![dbBrowser.PNG](https://bitbucket.org/repo/bEXb4L/images/3023751797-dbBrowser.PNG)

**Step Three: Running the Application**

The only remaining step to getting your development environment deployed is running the actual application. This can be achieved through the command ```python app.py```, when you run this command you should see a URL created for you. 

![alt text](image.png)

The URL will take you to the application and allow you to see any changes you make to the system. That's all that has to be done in order to get the development environment created and ready for editing.

[TOC]
#Installation#

##Requirements##
* python 2.7
* linux, unix, mac, windows(with attachments)
* git

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