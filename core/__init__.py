import os
import sys

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(app.root_path), 'core\\upload')

db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    from core.models import User
    user = User.query.get(int(user_id))
    return user


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("login.html", msg=request.args.get("msg", ""))

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"msg": "404 Not Found."}), 404

from core import commands, dashboard, user, trace, executor