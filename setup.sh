'''
This file sets up the virtual environment. 
Run "source setup.sh" each time you want to run the app. 
'''

mkdir -p data

if [ ! -d venv ]
then
  virtualenv venv
fi

. venv/bin/activate

sudo pip install Flask
sudo pip install peewee
sudo pip install pyyaml