from abc import ABC, abstractmethod
from typing import List, Optional
from models.entities.test1 import Test1

class IMysqlRepository(ABC):
    
    @abstractmethod
    async def create(self, connection, name) -> int:
        pass

    @abstractmethod
    async def create_with_cursor(self, cursor, name) -> int:
        pass

    @abstractmethod
    async def find_by_id(self, connection, id) -> Optional[Test1]:
        pass

    @abstractmethod
    async def find_by_id_with_cursor(self, cursor, id) -> Optional[Test1]:
        pass

    @abstractmethod
    async def update_by_id(self, connection, test1: Test1) -> int:
        pass

    @abstractmethod
    async def update_by_id_with_cursor(self, cursor, test1: Test1) -> int:
        pass

    @abstractmethod
    async def delete_by_id(self, connection, id) -> int:
        pass

    @abstractmethod
    async def delete_by_id_with_cursor(self, cursor, id):
        pass

class MysqlRepository(IMysqlRepository):
    async def create(self, connection, name) -> int:
        async with connection.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO test1 (test) VALUES (%s);",
                (name)
            )
            # await connection.commit()
            return cursor.lastrowid
        
    async def create_with_cursor(self, cursor, name) -> int:
        await cursor.execute(
            "INSERT INTO test1 (test) VALUES (%s);",
            (name)
        )
        return cursor.lastrowid
    
    async def find_by_id(self, connection, id) -> Optional[Test1]:
        async with connection.cursor() as cursor:
            await cursor.execute(
                "SELECT id, test FROM test1 WHERE id = %s;",
                (id)
            )
            row = await cursor.cursor()
            if not row:
                return None
            return Test1(**row)
    
    async def find_by_id_with_cursor(self, cursor, id) -> Optional[Test1]:
        await cursor.execute(
            "SELECT id, test FROM test1 WHERE id = %s;",
            (id)
        )
        row = await cursor.fetchone()
        if row in None:
            return None
        return Test1(**row)

    async def update_by_id(self, connection, test1: Test1) -> int:
        async with connection.cursor() as cursor:
            await cursor.execute(
                "UPDATE test1 SET test = %s WHERE id = %s;",
                (test1.id, test1.test)
            )
            return cursor.rowcount
    
    async def update_by_id_with_cursor(self, cursor, test1: Test1) -> int:
        await cursor.execute(
            "UPDATE test1 SET test = %s WHERE id = %s;",
            (test1.id, test1.test)
        )
        return cursor.rowcount

    async def delete_by_id(self, connection, id) -> int:
        async with connection.cursor() as cursor:
            await cursor.execute(
                "DELETE FROM test1 WHERE id = %s;",
                (id)
            )
            return cursor.rowcount
    
    async def delete_by_id_with_cursor(self, cursor, id):
        await cursor.execute(
            "DELETE FROM test1 WHERE id = %s;",
            (id)
        )
        return cursor.rowcount