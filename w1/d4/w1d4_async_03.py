# 四、asyncio 核心功能
# 1. asyncio.sleep() - 异步等待
import asyncio
import time


async def demo_sleep():
    print("开始等待...")
    await asyncio.sleep(2)  # 等待2秒，不阻塞其他任务
    print("等待完成")


# 2. asyncio.gather() - 并发执行
async def task1():
    await asyncio.sleep(1)
    return "任务1完成"


async def task2():
    await asyncio.sleep(2)
    return "任务2完成"


async def task3():
    await asyncio.sleep(1.5)
    return "任务3完成"


async def demo_gather():
    # 并发执行三个任务
    results = await asyncio.gather(task1(), task2(), task3())
    print(f"结果: {results}")
    # 总耗时约2秒 (最长的任务)


# 3. asyncio.create_task() - 创建任务
async def demo_create_task():
    # 创建任务
    task1_obj = asyncio.create_task(task1())
    task3_obj = asyncio.create_task(task3())

    # 等待任务完成
    result1 = await task1_obj
    result2 = await task3_obj

    print(f"结果: {result1}, {result2}")


# 4. asyncio.wait() - 等待多个任务
async def demo_wait():
    # 创建任务对象 (修复: 用 create_task 包装协程)
    tasks = [
        asyncio.create_task(task1()),
        asyncio.create_task(task2()),
        asyncio.create_task(task3())
    ]

    # 等待所有任务完成
    done, pending = await asyncio.wait(tasks)
    print(f"done: {len(done)}, pending: {len(pending)}")

    for task in done:
        print(f"完成: {task.result()}")


# 运行
async def main():
    print("=== demo_gather ===")
    start = time.time()
    await demo_gather()
    end = time.time()
    print(f"demo_gather耗时: {end - start:.1f}秒")  # 约2秒

    print("\n=== demo_create_task ===")
    start = time.time()
    await demo_create_task()
    end = time.time()
    print(f"create_task耗时: {end - start:.1f}秒")

    print("\n=== demo_demo_wait ===")
    start = time.time()
    await demo_wait()
    end = time.time()
    print(f"demo_wait耗时: {end - start:.1f}秒")


asyncio.run(main())
