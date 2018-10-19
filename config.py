# -*- coding:utf8 -*-
import os
import json


class ReadConfigJson(object):

    def __init__(self):
        path = os.path.abspath(os.path.dirname(__file__))
        config_path = os.path.join(path, 'config.json')
        self.config_path = config_path

    def __read_json(self):
        with open(self.config_path, encoding='utf-8') as f:
            data = f.read()
            data = json.loads(data)
        return data

    def get_mysql_config(self):
        mysql_dict = self.__read_json()['mysql']
        mysql_url = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8'.format(
            user=mysql_dict['user'],
            password=mysql_dict['password'],
            host=mysql_dict['host'],
            port=mysql_dict['port'],
            database=mysql_dict['database'])

        # return 'sqlite:////tmp/data.db'
        return mysql_url

    def get_ws_server_config(self):
        wsserver = self.__read_json()['ws_server']
        ws_server_url = '%s:%s' % (wsserver['ip'], wsserver['port'])
        return ws_server_url


class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = ReadConfigJson().get_mysql_config()
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
