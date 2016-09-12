import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://john:root@localhost/todo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {'production': ProductionConfig}
