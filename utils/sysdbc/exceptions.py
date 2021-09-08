from rest_framework import status
from rest_framework.exceptions import APIException

from utils.exceptions import TracebackApiException


class DbClientException(TracebackApiException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "DB client error"
    default_code = "unknown_error"


class DbConnectException(DbClientException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "error": "Can not connect {type} database",
        "database_setting": "{db_setting}",
        "response": "{response}",
    }
    default_code = "db_connect_fail"


class SqlExecuteResponseErrorException(DbClientException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {
        "error": "Database response {msg}",
        "request": "{request_data}",
        "response": "{response_data}",
    }
    default_code = 'unknown_error'


class UnSupportDatabaseTypeException(DbClientException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Unsupported database type: "{type}".'
    default_code = 'unknown_error'
