class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://event_planning_user:root1234@localhost:5432/event_planning_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Nequeporroquisquamestquidoloremipsumquiadolorsitametconsecteturadipiscivelit'
    JWT_ERROR_MESSAGE_KEY = 'LoremipsumdolorsitametconsecteturadipiscingelitNullamfermentumgravidaauctorInvelmetusquisnisiefficitursodalesnon'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']