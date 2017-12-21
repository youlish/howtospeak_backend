#!usr/bin/python2.7
from api.app import app
from api.caption import mod as caption
from api.videos import mod as videos
import os

app.register_blueprint(caption, url_prefix='/caption')
app.register_blueprint(videos, url_prefix='/videos')

@app.route('/')
def handle_defaule():
  return "OK"

if __name__=='__main__':
    app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 8080)))



