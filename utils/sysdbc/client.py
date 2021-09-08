# -*- coding: utf-8 -*-
from __future__ import absolute_import  # 絕對匯入

import os
import time

import jaydebeapi
import pandas as pd
import logging

from utils.sysdbc.exceptions import DbConnectException

logger = logging.getLogger('debug')
logger_scheduler = logging.getLogger('scheduler')


os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'


class DataBaseClient:
    def __init__(self, host, port, username=None, password=None):
        self.host = host
        self.port = port
        self.auth = [username, password]

        self.drivers = [
            'ojdbc8-19.9.0.0.jar',
            'mssql-jdbc-8.4.1.jre8.jar',
            'postgresql-42.2.18.jar',
            'mysql-connector-java-8.0.22.jar'
        ]
        self.driver_paths = [
            f'{os.path.dirname(os.path.realpath(__file__))}/driver/{d}' for d in self.drivers
        ]

        self.conn = None
        self.curs = None

    def connect(self, name):
        raise NotImplementedError()

    def _connect_and_set_cursor(self, java_driver_class, url, driver_args, driver_paths, db_type):
        """
        使用jaydebeapi.connect
        fixme 需持續追蹤db connect處
        :param java_driver_class:
        :param url:
        :param driver_args:
        :param driver_paths:
        :return:
        """
        try:
            self.conn = jaydebeapi.connect(
                jclassname=java_driver_class,
                url=url,
                driver_args=driver_args,
                jars=driver_paths,
            )
            self.curs = self.conn.cursor()

            if self.curs is None:
                logger.warning(f'DataBaseClient cursor got NoneType')
                raise DbConnectException(raiser=(self.__class__, self._connect_and_set_cursor), format={
                    "type": str(db_type),
                    "db_setting": f'host: {self.host}, port: {self.port}, username: {self.auth[0]}',
                    "response": "DataBaseClient cursor got NoneType",
                })
        except OSError as e:  # fixme 同時運行使用時，JVM檔案重複load錯誤
            logger.warning(f'jaydebeapi.connect() JVM loading occur OSError!\n{e}')
            raise DbConnectException(raiser=(self.__class__, self._connect_and_set_cursor), format={
                    "type": str(db_type),
                    "db_setting": f'host: {self.host}, port: {self.port}, username: {self.auth[0]}',
                    "response": str(e),
                })
        except Exception as e:
            logger.warning(f'jaydebeapi.connect() unknown error!\n{e}')
            raise DbConnectException(raiser=(self.__class__, self._connect_and_set_cursor), format={
                "type": str(db_type),
                "db_setting": f'host: {self.host}, port: {self.port}, username: {self.auth[0]}',
                "response": str(e),
            })

    def execute(self, sql):
        """
        return pd.DataFrame
        """
        # 去除換行及多於一個空白
        sql.replace('\r\n', '').replace('\n', '')
        sql = ' '.join(sql.split())
        self.curs.execute(sql)
        data = self.curs.fetchall()
        columns = [scheme[0] for scheme in self.curs.description]
        return pd.DataFrame(data=data, columns=columns)

    def close(self):
        self.curs.close()
        self.conn.close()


class OracleDbClient(DataBaseClient):
    def __init__(self, host, port, username, password):
        super(OracleDbClient, self).__init__(host, port, username, password)
        self.conn = None

    def connect(self, sid, driver_type='thin'):
        java_driver_class = 'oracle.jdbc.driver.OracleDriver'
        url = f'jdbc:oracle:{driver_type}:@{self.host}:{self.port}:{sid}'

        super()._connect_and_set_cursor(java_driver_class, url, self.auth, self.driver_paths, 'oracle')


class MicrosoftSqlClient(DataBaseClient):
    def __init__(self, host, port, username, password):
        super(MicrosoftSqlClient, self).__init__(host, port, username, password)
        self.conn = None

    def connect(self, name):
        java_driver_class = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'
        url = f'jdbc:sqlserver://{self.host}:{self.port}; databaseName={name}'

        super()._connect_and_set_cursor(java_driver_class, url, self.auth, self.driver_paths, 'mssql')


class PostgreSqlClient(DataBaseClient):
    def __init__(self, host, port, username, password):
        super(PostgreSqlClient, self).__init__(host, port, username, password)
        self.conn = None

    def connect(self, name):
        java_driver_class = 'org.postgresql.Driver'
        url = f'jdbc:postgresql://{self.host}:{self.port}/{name}'

        super()._connect_and_set_cursor(java_driver_class, url, self.auth, self.driver_paths, 'postgresql')


class MySqlClient(DataBaseClient):
    def __init__(self, host, port, username, password):
        super(MySqlClient, self).__init__(host, port, username, password)
        self.conn = None

    def connect(self, name):
        java_driver_class = 'com.mysql.cj.jdbc.Driver'
        url = f'jdbc:mysql://{self.host}:{self.port}/{name}'

        super()._connect_and_set_cursor(java_driver_class, url, self.auth, self.driver_paths, 'mysql')


# if __name__ == "__main__":
#     type0 = 'oracle'
#     host = '10.11.170.84'
#     port = '1521'
#     username = 'system'
#     password = 'oracle'
#     sid = 'orcl'
#     db = ''
#     client = OracleDbClient(f'{host}', f'{port}', f'{username}', f'{password}')
#     if type0 == 'oracle':
#         client.connect(sid=f'{sid}')
#     else:
#         client.connect(database_name=f'{db}')
#     r = client.execute('select * from dba_tables')
#     print(r)
#     client.close()
