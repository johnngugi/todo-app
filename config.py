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
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgres://kfajlmuyzwrxtq:dQCRdPb5XF9urQ2iIpe1vXFht0@ec2-54-243-204-129.compute-1.amazonaws.com:5432/d58pennmbbfm3h'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {'production': ProductionConfig}
