class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://noahismith:spotify-mmaps@spotify-mmaps.cnfthxsaxcoe.us-east-2.rds.amazonaws.com/spotifymmaps'


class LocalDevelopment(Config):
    DEBUG = True
    SQALCHEMY_ECHO = True
    CLIENT_SIDE_URL = "http://127.0.0.1:5000"


class Production(Config):
    DEBUG = False
    SQALCHEMY_ECHO = False
    CLIENT_SIDE_URL = "http://52.15.141.175"


class ServerDevelopment(Config):
    DEBUG = True
    SQALCHEMY_ECHO = True
    CLIENT_SIDE_URL = "http://52.15.141.175"


app_config = {
    'local': LocalDevelopment,
    'server': ServerDevelopment,
    'production': Production
}