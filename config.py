import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hell0Wor79'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or  'sqlite:///' + os.path.join(basedir, 'app.db')
    #SQLALCHEMY_DATABASE_URI ='postgres://idsaeucepvhhoi:01025df93c71cbb22330092e120db1561ef8ddc9fa7e4025b4a6c90a739768aa@ec2-50-19-109-120.compute-1.amazonaws.com:5432/d1sth1mo61q4c7'


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





