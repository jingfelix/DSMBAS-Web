import json
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from core import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    msg = db.Column(db.String(100), default='None')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_targets(self):
        return Target.query.filter_by(user_id=self.id).all()


class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    status = db.Column(db.Boolean, default=False)
    finish_time = db.Column(db.DateTime, default=None)
    user_id = db.Column(db.Integer)
    args = db.Column(db.String(100), default="")

    assigned = db.Column(db.Integer, default=0)
    warning = db.Column(db.Integer, default=0)
    error = db.Column(db.Integer, default=0)
    api_count = db.Column(db.Integer, default=0)

    info = db.Column(db.String(2000), default="")

    def load_info(self):
        # 返回info内容（python对象）

        if self.info == "":
            return {}

        return json.loads(self.info)
