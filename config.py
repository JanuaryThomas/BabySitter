import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hell0Wor79'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or  'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_DATABASE_URI ='postgres://btrlieuuhvhkdo:cab7f7798de7ba3b8f7347999269a73f7b547d77eb4f330dabcbc39f886f5c16@ec2-54-225-72-238.compute-1.amazonaws.com:5432/d2gvnmkvu7u57f'


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    #MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'pivothub2019@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'pivot@3232'
    ADMINS = ['pivothub2019@gmail.com']
    LANGUAGES = ['en', 'sw', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL ')


    MQTT_CLIENT_ID = "Intelects"
    MQTT_BROKER_URL = os.environ.get('MQTT_BROKER_URL') or 'm14.cloudmqtt.com'
    MQTT_BROKER_PORT = 16694
    MQTT_USERNAME = 'dfjbjrxg'
    MQTT_PASSWORD = 'tUHdAtaodcv7'
    MQTT_KEEPALIVE = 5
    MQTT_TLS_ENABLED = False


    # CKEDITOR
    DIR = os.path.join(os.path.dirname(__file__), 'app/static')
    CKEDITOR_FILE_UPLOADER = 'upload'
    UPLOADED_PATH = os.path.join(DIR, 'upload')

    SUPPORTED_LANGUAGES = {'sw': 'Swahili', 'en': 'English', 'fr': 'Francais'}
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'





