import os

class Config(object):
    SERCET_KEY = os.environ.get('SERCET_KEY') or 'bao-mat-cao@lennao'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
