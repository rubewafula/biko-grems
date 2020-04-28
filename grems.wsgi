#!/usr/bin/python
import os
import sys
import site
import logging
logging.basicConfig(stream=sys.stderr)

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/var/www/html/biko-grems/v/lib/python3.6/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/www/html/biko-grems')

# Activate your virtual env
#activate_env=os.path.expanduser("/var/www/html/biko-grems/v/bin/activate_this.py")
#execfile(activate_env, dict(__file__=activate_env))

from  app import app as application

