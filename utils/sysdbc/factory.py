from utils.sysdbc.exceptions import UnSupportDatabaseTypeException, DbConnectException
# from utils.sysdbc.client_v2 import MySqlClient, MicrosoftSqlClient, PostgreSqlClient, OracleDbClient, DataBaseConnectClient
from utils.sysdbc.client import MySqlClient, MicrosoftSqlClient, PostgreSqlClient, OracleDbClient, DataBaseClient


class DatabaseClientFactory:
    DB_TYPE_MYSQL = "mysql"
    DB_TYPE_POSTGRESQL = "postgresql"
    DB_TYPE_MSSQL = "mssql"
    DB_TYPE_ORACLE = "oracle"

    DB = {
        DB_TYPE_MYSQL: MySqlClient,
        DB_TYPE_MSSQL: MicrosoftSqlClient,
        DB_TYPE_POSTGRESQL: PostgreSqlClient,
        DB_TYPE_ORACLE: OracleDbClient,
    }

    @staticmethod
    def connect_db(type, host, port, username, password, name) -> DataBaseClient:
        """
        Database client factory method

        :param str type: 資料庫種類代稱
        :param str host:
        :param str port:
        :param str username:
        :param str password:
        :param str name:
        :return DataBaseClient:
        """
        try:
            db_client_clz = DatabaseClientFactory.DB[type]
        except KeyError:
            raise UnSupportDatabaseTypeException(
                raiser=(DatabaseClientFactory, DatabaseClientFactory.connect_db),
                format={
                    "type": type,
                }
            )

        try:
            db_client = db_client_clz(host, port, username, password)
            db_client.connect(name)
            return db_client
        except Exception as e:
            raise DbConnectException(
                raiser=(DatabaseClientFactory, DatabaseClientFactory.connect_db),
                format={
                    "type": str(type),
                    "db_setting": f'host: {host}, port: {port}, username: {username}',
                    "response": str(e),
                }
            )
