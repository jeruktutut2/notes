import unittest
from unittest.mock import AsyncMock, Mock
from repositories.mysql_repository import IMysqlRepository, MysqlRepository
from databases.mysql import IMysql
from services.mysql_service import IMysqlService, MysqlServive
from models.requests.create_request import CreateRequest

class TestMysqlService(unittest.IsolatedAsyncioTestCase):

    async def test_mysql_service_create(self):
        request = CreateRequest(test="test")
        fake_connection = Mock()
        fake_cursor = Mock()
        fake_commit = Mock()
        tests = [
            {
                "name": "begin transaction error",
                "request": request,
                "beginTransaction": Exception("internal server error"),
                "createWithCursor": Exception("internal server error"),
                "expected_result": None
            },
            {
                "name": "create with cursor error",
                "request": request,
                "beginTransaction": (fake_connection, fake_cursor),
                "createWithCursor": Exception("internal server error")
            },
            {
                "name": "commit error",
                "request": request,
                "beginTransaction": (fake_connection, fake_cursor),
                "createWithCursor": 1,
                "commit": Exception("internal service error")
            },
            {
                "name": "success",
                "request": request,
                "beginTransaction": (fake_connection, fake_cursor),
                "createWithCursor": 1,
                "commit": fake_commit
            }
        ]

        for tc in tests:
            print(f"=========== start {tc['name']} ===========")
            mysql = AsyncMock(spec=IMysql)
            print(1)
            if isinstance(tc['beginTransaction'], Exception): 
                print(2)
                mysql.begin_transaction.side_effect = tc['beginTransaction']
            else:
                print(3)
                mysql.begin_transaction.return_value = tc['beginTransaction']
            print(4)
            mysql_repository = AsyncMock(spec=IMysqlRepository)
            print(5)
            mysql_repository.create_with_cursor.side_effect = tc['createWithCursor']
            print(6)
            # mysql_repository.begin_transaction.side_effect = tc['beginTransaction']
            mysql_service = MysqlServive(mysql, mysql_repository)
            print(7)
            # result = await mysql_service.create(tc['request'])
            # print(f"result: {result}")
            # self.assertEqual(result, tc["expected_result"])
            with self.assertRaises(Exception):
                await mysql_service.create(tc['request'])
            print(f"=========== end {tc['name']} ===========")
