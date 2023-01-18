from functools import wraps

from logger import LOGGER


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        LOGGER.info(f'REQUEST: {result.request.method}: {result.request.url}')
        if result.request.method in ['POST', 'PUT', 'PATCH']:
            LOGGER.info(f'REQUEST_DATA: {result.request.body}')
        LOGGER.info(f'CONTENT: {result.status_code}":" {result.content}')
        return result

    return wrapper


class BaseApi:
    session = None

    @logger
    def get(self, link, params=None, headers=None):
        return self.session.get(url=link, params=params, headers=headers)

    @logger
    def post(self, link, params=None, json=None, headers=None):
        return self.session.post(url=link, params=params, json=json, headers=headers)

    @logger
    def put(self, link, params=None, json=None, headers=None):
        return self.session.put(url=link, params=params, json=json, headers=headers)
