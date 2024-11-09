class Config:
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5000
    COMPRESSION_QUALITY = 60
    SCALE_FACTOR = 0.75

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}