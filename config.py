import os

basedir = os.path.abspath(os.path.dirname(__file__))


<<<<<<< HEAD
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL', 'postgresql:///Cap1'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

=======
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL', 'postgresql:///Cap1'))
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'TEST_KEY'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL', 'postgresql:///Cap1_test'))
    WTF_CSRF_ENABLED = False

>>>>>>> e7e0204 (Added Testing)

