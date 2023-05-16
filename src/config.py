import dotenv
import os

dotenv.load_dotenv()

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
HOST = os.environ.get('HOST')
# SECRET = os.environ.get('SECRET')

#
DB_CONFIG = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?async_fallback=True"