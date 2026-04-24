# 三、async/await 基础
import asyncio


# 1. 定义异步函数
async def hello():
    return "Hello, World!"


# 2. 调用异步函数
async def main():
    result = await hello()  # 使用 await 调用
    print(result)


asyncio.run(main())


# 3. 异步函数的特点
async def fetch_data():
    print("开始获取数据...")
    await asyncio.sleep(1)  # 模拟网络请求
    print("数据获取完成")
    return {"data": "some data"}


async def process_data():
    print("开始处理数据...")
    await asyncio.sleep(0.5)  # 模拟处理
    print("数据处理完成")
    return "processed"


# 4. 异步函数链式调用
async def main():
    data = await fetch_data()
    print(f"获取数据结果: {data}")
    result = await process_data()
    print(f"最终结果: {result}")


asyncio.run(main())
