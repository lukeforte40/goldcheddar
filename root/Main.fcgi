#!$home/python-install-workspace/python-3.8.5
import sys
sys.path.insert(0, '$home/GoldCheddar/root/main.py')

from flup.server.fcgi import WSGIServer
from index import app

class ScriptNameStripper(object):
   def __init__(self, app):
       self.app = app

   def __call__(self, environ, start_response):
       environ['SCRIPT_NAME'] = ''
       return self.app(environ, start_response)

app = ScriptNameStripper(app)

if __name__ == '__main__':
    WSGIServer(app).run()