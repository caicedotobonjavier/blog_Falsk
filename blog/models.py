from blog import db
#
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(200))
    post = db.relationship('Post', uselist=False, back_populates='user', cascade='all, delete-orphan', single_parent=True)

    def __init__(self, username, email, password, photo=None):
        self.username = username
        self.email = email
        self.password = password
        self.photo = photo

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    info = db.Column(db.Text)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    user = db.relationship('User', back_populates='post', single_parent=True)
    

    def __init__(self, author, url, title, info, content):
        self.author = author
        self.url = url
        self.title = title
        self.info = info
        self.content = content

    def __repr__(self):
        return f'<Post {self.title}>'