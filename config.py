#configruacion de la base de datos a la cual me voy a conectar, puedo usar varias y cambiarlas en la Confgi
SQLITE = "sqlite:///blogflaskdb.db"
POSRTGRESQL = 'postgresql://postgres:88052571620ja@localhost:5432/blogflaskdb'

class Config:
    DEBUG = True
    SECRET_KEY = 'JAVIER'
    #conexion_BASE_DATOS
    SQLALCHEMY_DATABASE_URI = POSRTGRESQL

    CKEDITOR_PKG_TYPE = 'full'
