import os
from dotenv import load_dotenv

load_dotenv()

APP_PORT = os.getenv("APP_PORT")

az_detail = {
    "STORAGE_ACCOUNT_NAME": os.getenv("STORAGE_ACCOUNT_NAME"),
    "MODEL_CONTAINER_NAME": os.getenv("MODEL_CONTAINER_NAME"),
    "ACCOUNT_KEY": os.getenv("ACCOUNT_KEY"),
    "CONNECTION_STRING": os.getenv("CONNECTION_STRING"),
}

auth = {
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "ALGORITHM": os.getenv("ALGORITHM"),
    "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")),
    "REFRESH_TOKEN_EXPIRE_DAYS": int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")),
    "ISSUER": os.getenv("ISSUER"),
    "AUDIENCE": os.getenv("AUDIENCE"),
}

db = {
    "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
    "POSTGRES_PORT": os.getenv("POSTGRES_PORT"),
    "POSTGRES_USER": os.getenv("POSTGRES_USER"),
    "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    "POSTGRES_DB": os.getenv("POSTGRES_DB"),
    "POSTGRES_SCHEMA": os.getenv("POSTGRES_SCHEMA")
}
print("db: ", db)

