import os

DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))
# where front end codes are
RIOT_ROOT = os.path.join(basedir, 'riot_front')
# template folder location
TEMPLATE_FOLDER = os.path.join(RIOT_ROOT, "app")
# 30 minute session timeout
PERMANENT_SESSION_LIFETIME = 30 * 60 

