# 六、异步上下文管理器
# 异步上下文管理器 - async with
import asyncio


class AsyncDatabaseConnection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.connection = None

    async def __aenter__(self):
        print(f"连接数据库: {self.db_url}")
        await asyncio.sleep(0.5)  # 模拟连接
        self.connection = {"status": "connected"}
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("关闭数据库连接")
        await asyncio.sleep(0.1)  # 模拟关闭
        self.connection = None

    async def query(self, sql):
        print(f"执行查询: {sql}")
        await asyncio.sleep(0.2)  # 模拟查询
        return [{"id": 1, "name": "张三"}]


# 使用
async def main():
    async with AsyncDatabaseConnection("mysql://localhost:3306/mydb") as db:
        result = await db.query("SELECT * FROM users")
        print(f"查询结果: {result}")


asyncio.run(main())
