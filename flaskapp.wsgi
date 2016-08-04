activate_this= '/var/www/html/bcsr-flask/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/bcsr-flask/")
# from app import app
from app import app as application
