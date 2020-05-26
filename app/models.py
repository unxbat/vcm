from app import db, login, app
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
#    first_name = db.Column(db.String(64), index=True, nullable=True)
#    second_name = db.Column(db.String(64), index=True, nullable=True)
    videos = db.relationship('Video', backref='author', lazy='dynamic')

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(48), index=True)
    category = db.Column(db.String(48), index=True)
    path = db.Column(db.String(128))
    full_path = db.Column(db.String(128))
    description = db.Column(db.String(140), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.String(16), )
    size = db.Column(db.String, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def set_duration(self, info):
        self.duration = info['duration']

    def set_size(self, info):
        self.size = info['size']


