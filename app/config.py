import os

from dotenv import load_dotenv


load_dotenv()


APP_NAME = os.getenv("APP_NAME", "Mini Agent")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
MY_API_KEY = os.getenv("MY_API_KEY")