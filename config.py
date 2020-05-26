#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os


BASEDIR = os.path.abspath((os.path.dirname(__file__)))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "ohuenno_slozhniy_secret_key"
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///media.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = os.path.join(BASEDIR, 'static')
    STATIC_URL_PATH = '/static'
    TEMPLATES_AUTO_RELOAD = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql//{user}:{password}@{host}:{port}/{dbname}'.format(user='',
    #                                                                                         password='',
    #                                                                                         host='localhost',
    #                                                                                         port='5432',
    #                                                                                         dbname=''
    #                                                                                         )


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True