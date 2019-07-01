'''
This file sets up the virtual environment. 
Run "source setup.sh" each time you want to run the app. 
'''
FLASK_VERSION="${FLASK_VERSION:-0.12.2}"              #0.12.2
PEEWEE_VERSION="${PEEWEE_VERSION:-2.10.2}"            #2.10.2
PYAML_VERSION="${PYAML_VERSION:-3.12}"                #3.12
XLSXWRITER_VERSION="${XLSXWRITER_VERSION:-1.0.2}"     #1.0.2
FLASK_ADMIN_VERSION="${FLASK_ADMIN_VERSION:-1.5.0}"   #1.5.0
WTF_PEEWEE_VERSION="${WTF_PEEWEE_VERSION:-0.2.6}"     #0.2.6

mkdir -p data

if [ ! -d venv ]
then
  virtualenv venv
fi

. venv/bin/activate

pip install flask
pip install peewee
pip install pyyaml
pip install XlsxWriter
pip install flask-admin
pip install wtf-peewee
pip install jinja2
pip install itsdangerous
pip install click
