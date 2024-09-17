from flask import Blueprint, render_template, request, redirect, url_for, g, session, flash
#
from blog import db
#
from .models import Post
#
from .auth import  login_required

bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/posts')
@login_required
def posts():
    all_posts = Post.query.filter_by(author=g.user.id)

    return render_template('admin/posts.html', posts=all_posts)


@bp.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        author = g.user.id,
        url = request.form['url']
        url = url.replace(' ', '-')
        title = request.form['title']
        info = request.form['info']
        data = request.form.get('ckeditor')
        
        url_create = Post.query.filter_by(url=url).first()
        if not url_create:
            post = Post(
                author=author,
                url=url,
                title=title,
                info=info,
                content=data
            )

            db.session.add(post)
            db.session.commit()

            flash(f'Post {title} creado correctamente')
            return redirect(url_for('post.posts'))
        else:
            flash(f'La url {url} ya existe')
            return redirect(url_for('post.create'))
        
    return render_template('admin/create.html')



@bp.route('/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update(id):
    update_post = Post.query.get(id)
    if request.method=="POST":
        update_post.url = request.form['url']
        update_post.title = request.form['title']
        update_post.info = request.form['info']
        update_post.content = request.form.get('ckeditor')
        db.session.commit()
        flash(f'Post {update_post.title} actualizado correctamente')
        return redirect(url_for('post.posts'))
    
    return render_template('admin/update.html', post=update_post)


@bp.route('delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post {post.title} eliminado correctamente')
    return redirect(url_for('post.posts'))