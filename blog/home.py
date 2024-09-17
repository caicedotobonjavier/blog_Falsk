from flask import Blueprint, render_template, request, redirect, url_for, session, g
#
from blog import db
#
from .models import User, Post

bp = Blueprint('home', __name__)



#filtros perzonalizados para usar en los templates y registrarlos para usarlos
@bp.add_app_template_filter
def today(date):
    return date.strftime('%d de %m-%Y')


def get_user(id):
    user = User.query.get(id)
    return user


def search_post(dato):
    posts = Post.query.filter(Post.title.ilike(f'%{dato}%')).all()
    return posts

@bp.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.all()

    if request.method == 'POST':
        posts = search_post(request.form['search'])
        value = 'hidden'
        return render_template('index.html', posts=posts, get_user=get_user, search_post=search_post, value=value)
    
    return render_template('index.html', posts=posts, get_user=get_user, search_post=search_post)


@bp.route('/blog/<url>')
def blog(url):
    post = Post.query.filter_by(url=url).first()
    return render_template('blog.html', post=post, get_user=get_user)


