from flask import Flask
#
from flask_sqlalchemy import SQLAlchemy


#INTANCIAR LA BASE DE DATOS
db = SQLAlchemy()

def create_app():
    #crear la app
    app = Flask(__name__)


    #llamo la condiguracion del proyecto
    app.config.from_object('config.Config')

    #Inicializo base de datos
    db.init_app(app)

    #inicializo ckeditor
    #
    from flask_ckeditor import CKEditor
    ckeditor = CKEditor(app)

    # idiioma
    import locale
    locale.setlocale(locale.LC_ALL, 'es_ES')


    #creo las urls blueprint
    from . import home
    app.register_blueprint(home.bp)
    #
    from . import auth
    app.register_blueprint(auth.bp)
    #
    from . import post
    app.register_blueprint(post.bp)

    #importo modelos para que se creen las tablas en al base de datos
    from . import models

    @app.route('/')
    def index():
        return 'Hola Blog'

    with app.app_context():
        db.create_all()



    return app