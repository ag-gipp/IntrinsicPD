import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Assumed that directory <container> contains both the 
# plagapp directory and the plagcomps (actual processing)
# directory as well. Override this if the plagcomps
# repo lives elsewhere
PLAGCOMPS_LOC = os.path.dirname(basedir)
APP_ROOT = os.path.join(basedir, 'app')
CSRF_ENABLED = True
SECRET_KEY = 'SOME SECRET!!'
