from flask import Flask, current_app, url_for, jsonify
from .caption import mod as caption
from .videos import mod as videos
from .category import mod as video_categories


app = Flask(__name__)

app.register_blueprint(caption, url_prefix='/caption')
app.register_blueprint(videos, url_prefix='/videos')
app.register_blueprint(video_categories, url_prefix='/videocategories')


@app.route('/')
def handle_default():
    from urllib.parse import urlparse
    output = []
    for rule in current_app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urlparse("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print (line)
    return jsonify(urls=output)
