import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_APP = os.getenv("FLASK_APP")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    FLASK_ENV = os.getenv("FLASK_ENV")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")

    pokemontcgsdk_api_key = os.getenv("POKEMONTCG_IO_API_KEY")
