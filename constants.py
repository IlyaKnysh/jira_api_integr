import os

from dotenv import load_dotenv

load_dotenv()


def get(key, default=None):
    return os.environ.get(key=key, default=default)


BASE_URL = get('URL', '')
PROJECT_NAME = get('PROJECT_NAME', 'LCP')
AUTH = get('AUTH', '')
