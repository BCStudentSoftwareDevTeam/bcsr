## Built With

* [Flask](http://flask.pocoo.org/docs/0.11/)  - Python Based Web Framework Used
* [Jinja2](http://jinja.pocoo.org/docs/dev/) - HTML Templating Language for Python
* [Peewee](http://docs.peewee-orm.com/en/latest/index.html) - A small, expressive ORM used for database communications
* [SQLite](https://sqlite.org/) - SQL database engine

## Setting Up a Linux Development Environment on Windows
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

**Step Two: Ensure you have Python installed**

From WSL/Ubuntu, check whether Python is installed: ```python3 --version```

You can also check pip: ```pip3 --version```

If Python is not installed, install Python and the packages required to create virtual environments:
``` bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

After installation, verify it again: ```python3 --version```

>After the steps are complete, continue to running the application section

## Setting Up a Linux Development Environment on MacOS

### Getting Started With MacOS ###

Homebrew is a package manager for macOS and makes it easier to install development tools such as Python, Git, and MySQL.

- First, check whether Homebrew is already installed: ```brew --version```
- If you receive: ```command not found: brew```
- Install Homebrew by running the following command in Terminal:  ```/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"```
- Then verify that Homebrew is installed: ```brew --version```

### Getting Your Development Environment Running

After you have ensure homebrew is installed, there are additional steps that you will have to complete before your virtual environment will be completely operational. 

**Step One: Ensure You Have MySQL Installed**

- Check whether MySQL is installed: ```mysql --version```
- You can also check whether MySQL was installed through Homebrew: ```brew list | grep mysql```
- If MySQL is not installed, you can install it using the official MySQL graphical installer for macOS.
- Go to the MySQL Community Server download page: https://dev.mysql.com/downloads/mysql/

Select macOS as the operating system.
Download the DMG Archive that matches your Mac.
- Apple Silicon Macs use ARM64.
- Intel Macs use x86_64.

Open the downloaded .dmg file and run the MySQL installer.
Follow the installation prompts.

During setup, create a password for the MySQL root user.

For the BCSR development environment, if the project configuration expects:
- Username: root
- Password: root

you can set the root password to root, or update app/secret_config.yaml to match the password you choose.

After installation, verify MySQL from Terminal: ```mysql --version```

You can also test the connection with: ```mysql -u root -p```

Enter the root password you created during installation.

**Step Two: Ensure You Have Python Installed**

Check your installed Python version and pip: 
```bash
python3 --version
pip3 --version
```

If Python is not installed, you can install it using Homebrew which is also installed pip: ```brew install python```

After installation, verify the version: ```python3 --version```

## Steps to run the BCSR application

Navigate to your BCSR repository e.g.: ```cd ~/Desktop/SSDT/bcsr``

For Window: in order to do this, first you need to be in Ubuntu so run in your terminal: ```wsl```. Then run: ```source setup.sh```

For MacOS, you just need to run: ```source setup.sh```

After setup is complete, you should see:
- If you have this error: `-bash: setup.sh: line <something>: syntax error: unexpected end of file from "if" command on line 19` go to the bottom of your IDE and find CRLF and click it to select  LF

- ![venv.PNG](https://bitbucket.org/repo/bEXb4L/images/2846617267-venv.PNG) 

>***Note:*** 
In order for the application to work, you must activate the virtual environment. If you are not inside of the virtual environment you will see this error:

![venvError.PNG](https://bitbucket.org/repo/bEXb4L/images/1415469357-venvError.PNG)

Whenever you get this error just activate the virtual environment again by entering the command ```source setup.sh```

>***Note:***
Also, If you ever want to deactivate the virtual environment for any reason just type ```deactivate``` into the terminal:

![deactivate.PNG](https://bitbucket.org/repo/bEXb4L/images/2248015321-deactivate.PNG)

**Step Four: Setup Your Database**

**Create Database**
> **WARNING:** `create_db.py` is intended for development setup. Do not run this script against a production environment after real data exists.

 By typing the command ```python create_db.py``` or ```python3 create_db.py``` a database file containing the correct schemas will be created in the data directory for development setup.

**How to View the Database** 

To access MySQL from the terminal, run: ```mysql -u root -proot```

Once connected, you should see the MySQL prompt: ```mysql> ```

**Step Five: Running the Application**

The only remaining step to getting your development environment deployed is running the actual application. This can be achieved through the command ```python app.py``` or ```python3 create_db.py```, when you run this command you should see a URL created for you. 

The URL will take you to the application and allow you to see any changes you make to the system. That's all that has to be done in order to get the development environment created and ready for editing.

## Working with the flask template ##
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

[TOC]
#Installation#

##Requirements##
* python 3.11+
* linux, unix, mac, windows(with attachments)
* git