import os # noqa

from pymongo import MongoClient # noqa

from TeleBot.settings.base import *  # noqa

DEBUG = True

ALLOWED_HOSTS.append("telebot-p4.herokuapp.com")

mongodb_user = os.getenv("MONGO_USER")
mongodb_password = os.getenv("MONGO_PASSWORD")
mongodb_host = os.getenv("MONGO_HOST")
MONGO_CLIENT = MongoClient(
    f"mongodb+srv://{mongodb_user}:{mongodb_password}@{mongodb_host}"
)
MONGO_DB = MONGO_CLIENT.TeleBot
