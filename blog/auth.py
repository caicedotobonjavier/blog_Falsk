from flask import Blueprint, render_template, request, flash, redirect, url_for, g, session
#
from werkzeug.security import check_password_hash, generate_password_hash
#
from .models import User
#
from blog import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        usuario = User(
            username = username,
            email = email,
            password = generate_password_hash(password)
        )

        user_mail = User.query.filter_by(email=email).first()
        if not user_mail:
            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash(f'el Email {email} ya registrado')
            return redirect(url_for('auth.register'))
        
    return render_template('auth/register.html')

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']

        usuario = User.query.filter_by(email=email).first()
        if usuario:
            if check_password_hash(usuario.password, password):
                session.clear()
                session['user_id'] = usuario.id
                return redirect(url_for('home.index'))

            elif not check_password_hash(usuario.password, password):
                flash('Usuario o contraseña incorreta')
                return redirect(url_for('auth.login'))
            
            elif not usuario:
                flash('Usuario o contraseña incorreta')
                return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


import functools
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


#editar perfil
from werkzeug.utils import secure_filename

def get_image(id):
    user = User.query.get_or_404(id)
    return user.photo



@bp.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    usuario = User.query.filter_by(id=g.user.id).first()
    
    if request.method=='POST':            
        if request.form['username'] and request.form['password'] and request.files['photo']:
            usuario.username = request.form['username']        
            password = request.form['password']
            usuario.password = generate_password_hash(password)
            photo = request.files['photo']
            photo.save(f'blog/media/{secure_filename(photo.filename)}')
            usuario.photo = f'media/{secure_filename(photo.filename)}'
            db.session.commit()
            flash('Datos actualizados')
            session.clear()
            return redirect(url_for('auth.login'))
        
        elif request.form['username'] and request.form['password']=='' and request.files['photo']=='':
            usuario.username = request.form['username']
            db.session.commit()
            flash('Datos actualizados')

        elif request.form['password']:
            password = request.form['password']
            usuario.password = generate_password_hash(password)
            db.session.commit()
            flash('Datos actualizados')
            session.clear()
            return redirect(url_for('auth.login'))
        
        elif request.files['photo']:
            print('me meti a foto')
            photo = request.files['photo']
            photo.save(f'blog/static/media/{secure_filename(photo.filename)}')
            usuario.photo = f'media/{secure_filename(photo.filename)}'
            db.session.commit()
            flash('Datos actualizados')
            return redirect(url_for('auth.profile'))
        
    return render_template('auth/profile.html')


