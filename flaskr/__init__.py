import os
from flask import Flask, render_template, redirect, abort
from pathlib import Path
from dotenv import load_dotenv
from flask_cors import CORS
from .Models.models import app_config


# Set env directory
env_folder = Path(Path(__file__).parent).parent
env_file = os.path.join(env_folder, '.env')
load_dotenv(dotenv_path=env_file)


def create_app():
    # Create app
    app = Flask(__name__, static_folder='frontend/static', template_folder='frontend')

    # Setup Database, LoginManager, and Bcrypt
    app_config(app)

    # Setup CORS
    CORS(app, resources={r'/*': {'origins': 'http://localhost:3000'}})

    @app.after_request
    def after_request(resp):
        resp.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
        resp.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS,PATCH')

        return resp

    # Register Blueprints
    from flaskr.Errors.handlers import errors
    from flaskr.URLCut.routes import shorten

    app.register_blueprint(errors)
    app.register_blueprint(shorten)

    @app.route('/')
    def index():
        return render_template('index.html')

    from flaskr.Models.models import ShortURL

    @app.route('/<short_url>')
    def redirect_to_url(short_url):
        link = ShortURL.query.filter_by(short_url=short_url).first()

        if not link:
            abort(400, 'This Link is Not Available!')

        return redirect(link.original_url)

    return app
