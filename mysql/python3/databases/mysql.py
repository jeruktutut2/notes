from typing import Optional, Dict, Any
import aiomysql
from abc import ABC, abstractmethod
from aiomysql import Pool, DictCursor
from aiomysql.connection import Connection

class IMysql(ABC):

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def get_connection(self) -> Connection:
        pass

    @abstractmethod
    async def get_connection_and_cursor(self):
        pass

    # @abstractmethod
    # async def begin_transaction(self) -> Connection:
        # pass

    @abstractmethod
    async def begin_transaction(self):
        pass

    @abstractmethod
    async def commit(self, connection):
        pass

    @abstractmethod
    async def rollback(self, connection):
        pass

    @abstractmethod
    async def close_cursor(self, cursor):
        pass

    @abstractmethod
    async def release(self, connection):
        pass

    # @abstractmethod
    # async def close_cursor(self, cursor):
        # pass

    @abstractmethod
    async def close(self):
        pass
    


class Mysql(IMysql):

    _pool: Optional[Pool] = None
    # _config: dict = dict()
    _config: Dict[str, Any]

    def __init__(self, host: str, username: str, password: str, database: str, port: int, minimize: int = 1, maximise: int = 5):
        # pass
        self._config = {
            "host": host,
            "port": port,
            "user": username,
            "password": password,
            "db": database,
            "minsize": minimize,
            "maxsize": maximise,
            "autocommit": True,
        }
    
    async def connect(self):
        if not self._pool:
            self._pool = aiomysql.create_pool(**self._config)
    
    async def get_connection(self) -> Connection:
        connection = await self._pool.acquire()
        return connection
    
    async def get_connection_and_cursor(self):
        connection = await self._pool.acquire()
        cursor = connection.cursor()
        return connection, cursor
    
    # async def begin_transaction(self) -> Connection:
        # connection = await self._pool.acquire()
        # connection.autocommit = False
        # cursor = await connection.cursor(DictCursor)
        # return connection, cursor
    
    async def begin_transaction(self, isolation="SERIALIZABLE"):
        connection = await self._pool.acquire()
        connection.autocommit = False
        cursor = await connection.cursor(DictCursor)

        # Set isolation level SERIALIZABLE
        await cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL " + isolation)

        return connection, cursor
    
    async def commit(self, connection):
        return await connection.commit()
    
    async def rollback(self, connection):
        return await connection.rollback()
    
    async def close_cursor(self, cursor):
        return await cursor.close()

    async def release(self, connection):
        return self._pool.release(connection)
        
    async def close(self):
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()