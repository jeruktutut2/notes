from abc import ABC, abstractmethod
from models.results.result import Result
from models.requests.create_request import CreateRequest
from repositories.mysql_repository import MysqlRepository
from databases.mysql import Mysql
from models.requests.update_request import UpdateRequest
from models.entities.test1 import Test1

class IMysqlService(ABC):

    @abstractmethod
    async def create(self, create_request: CreateRequest) -> Result:
        pass

    @abstractmethod
    async def find_by_id(self, id) -> Result:
        pass

    @abstractmethod
    async def update_by_id(self, update_request: UpdateRequest) -> Result:
        pass

    @abstractmethod
    async def delete_by_id(self, id) -> Result:
        pass

class MysqlServive(IMysqlService):
    mysql: Mysql
    mysql_repository: MysqlRepository

    def __init__(self, mysql: Mysql, mysql_repository: MysqlRepository):
        self.mysql = mysql
        self.mysql_repository = mysql_repository
    
    async def create(self, create_request: CreateRequest) -> Result:
        print(1)
        connection = None
        cursor = None
        try:
            print(2)
            # connection = await self.mysql.get_connection()
            connection, cursor = await self.mysql.begin_transaction()
            # connection.autocommit = False
            # lastrowid = await self.mysql_repository.create(connection, create_request.test)
            print(3)
            lastrowid = await self.mysql_repository.create_with_cursor(cursor, create_request.test)
            # await self.mysql_repository.delete_by_id_with_cursor()
            # await connection.commit()
            print(4)
            await self.mysql.commit(connection)
            print(5)
            return Result(id=lastrowid, test=create_request.test)
        except Exception as e:
            if connection is not None:
                # await connection.rollback()
                await self.mysql.rollback(connection)
            raise e
        finally:
            if cursor is not None:
                await self.mysql.close_cursor(cursor)
            if connection is not None:
                connection.autocommit = True
                # self.mysql._pool.release(connection)
                self.mysql.release(connection)
    
    async def find_by_id(self, id) -> Result:
        connection = None
        cursor = None
        try:
            # connection = await self.mysql.get_connection()
            connection, cursor = await self.mysql.get_connection_and_cursor()
            # test1 = await self.mysql_repository.find_by_id(connection, id)
            test1 = await self.mysql_repository.find_by_id_with_cursor(cursor, id)
            return Result(id=test1.id, test=test1.test)
        except Exception as e:
            # if connection is not None:
                # await connection.rollback()
            raise
        finally:
            if cursor is not None:
                await self.mysql.close_cursor(cursor)
            
            if connection is not None:
                # self.mysql._pool.release(connection)
                self.mysql.release(connection)
    
    async def update_by_id(self, update_request: UpdateRequest) -> Result:
        connection = None
        cursor = None
        try:
            # connection = await self.mysql.get_connection()
            connection, cursor = await self.mysql.begin_transaction()
            # connection.autocommit = False
            test1 = Test1(id=update_request.id, test=update_request.test)
            # rows_affected = await self.mysql_repository.update_by_id(connection, test1)
            rows_affected = await self.mysql_repository.update_by_id_with_cursor(cursor, test1)
            if rows_affected != 1:
                raise ValueError("rows affected is not 1")
            
            await self.mysql.commit(connection)
            return Result(id=test1.id, test=test1.test)
        except Exception as e:
            if connection is not None:
                # await connection.rollback()
                await self.mysql.rollback(connection)
            raise
        finally:
            if cursor is None:
                await self.mysql.close_cursor(cursor)
            if connection is not None:
                connection.autocommit = True
                # self.mysql._pool.release(connection)
                self.mysql.release(connection)
    
    async def delete_by_id(self, id) -> Result:
        connection = None
        cursor = None
        try:
            connection, cursor = await self.mysql.begin_transaction()
            rows_affected = await self.mysql_repository.delete_by_id_with_cursor(cursor, id)
            if rows_affected != 1:
                raise ValueError("rows affected is not 1")
            await self.mysql.commit(connection)
            return None
        except Exception as e:
            if connection is not None:
                await self.mysql.rollback(connection)
            raise
        finally:
            if cursor is not None:
                await self.mysql.close_cursor(cursor)
            if connection is not None:
                connection.autocommit = True
                self.mysql.release(connection)
                

                 
