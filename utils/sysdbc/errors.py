# -*- coding: utf-8 -*-


class SysdbcException(RuntimeError):
    def __init__(self, msg):
        super(SysdbcException, self).__init__(msg)


class ConnectError(SysdbcException):
    pass


class ExecuteError(SysdbcException):
    pass