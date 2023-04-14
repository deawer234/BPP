import os
from flask import Flask, session
from website.website import website_api
import sys;
from website.database.database import init_db
from website.model.robot_controll import pi

os.environ["PIGPIO_ADDR"] = "192.168.0.80"
app = Flask(__name__)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    init_db()
    app.template_folder = 'templates'
    app.register_blueprint(website_api)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    return app

@app.teardown_appcontext
def close_pi(error):
    pi.stop()