# 二、同步 vs 异步
# 同步代码 (阻塞)
import time


def sync_task(name, seconds):
    print(f"开始任务: {name}")
    time.sleep(seconds)  # 阻塞等待
    print(f"完成任务: {name}")
    return f"{name}的结果"


# 同步执行 - 总共需要 3 秒
start = time.time()
result1 = sync_task("任务1", 1)
result2 = sync_task("任务2", 1)
result3 = sync_task("任务3", 1)
end = time.time()
print(f"同步耗时: {end - start:.1f}秒")  # 约6秒

# 异步代码 (非阻塞)
import asyncio


async def async_task(name, seconds):
    print(f"开始任务: {name}")
    await asyncio.sleep(seconds)  # 非阻塞等待
    print(f"完成任务: {name}")
    return f"{name}的结果"


# 异步执行 - 总共只需要 1 秒
async def main():
    start = time.time()

    # 并发执行三个任务
    results = await asyncio.gather(
        async_task("任务1", 1),
        async_task("任务2", 1),
        async_task("任务3", 1)
    )

    end = time.time()
    print(f"异步耗时: {end - start:.1f}秒")  # 约2秒
    print(f"结果: {results}")


asyncio.run(main())
