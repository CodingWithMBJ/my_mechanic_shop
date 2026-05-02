
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()


db_user = os.getenv("DB_USER")
db_pass = quote_plus(os.getenv("DB_PASSWORD", ""))
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}/{db_name}"
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    
class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class ProductionConfig:
    pass
    

