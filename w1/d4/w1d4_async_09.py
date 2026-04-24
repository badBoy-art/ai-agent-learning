# 十一、错误处理
import asyncio


async def risky_task(name, should_fail=False):
    if should_fail:
        raise ValueError(f"{name} 任务失败!")
    await asyncio.sleep(1)
    return f"{name} 完成"


async def main():
    # 1. 单个任务的错误处理
    try:
        result = await risky_task("任务1", should_fail=True)
    except ValueError as e:
        print(f"捕获错误: {e}")

    # 2. 并发任务的错误处理
    tasks = [
        risky_task("任务A"),
        risky_task("任务B", should_fail=True),
        risky_task("任务C")
    ]

    # 使用 return_exceptions=True 收集所有结果
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"任务{i + 1} 失败: {result}")
        else:
            print(f"任务{i + 1} 成功: {result}")


asyncio.run(main())
