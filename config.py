from flask_migrate import Config
import os

class Config:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ERROR_MESSAGE_KEY = 'LoremipsumdolorsitametconsecteturadipiscingelitNullamfermentumgravidaauctorInvelmetusquisnisiefficitursodalesnon'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

class DevConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://event_planning_user:root1234@localhost:5432/event_planning_db"
    SECRET_KEY = 'Nequeporroquisquamestquidoloremipsumquiadolorsitametconsecteturadipiscivelit'

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_2')
    SECRET_KEY = os.environ.get('SECRET_KEY')