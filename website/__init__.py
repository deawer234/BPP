import os
from flask import Flask, session
from website.website import website_api

app = Flask(__name__)

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.template_folder = 'templates'

    app.register_blueprint(website_api)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    return app