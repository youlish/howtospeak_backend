#!flask/bin/python
from app import app
from api.caption import mod as caption
from api.videos import mod as videos

app.register_blueprint(caption, url_prefix='/caption')
app.register_blueprint(videos, url_prefix='/videos')

if __name__=='__main__':
    app.run(debug=True)



