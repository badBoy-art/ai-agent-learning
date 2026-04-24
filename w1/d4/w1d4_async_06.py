# 七、异步迭代器
# 异步迭代器 - async for
import asyncio


class AsyncRange:
    def __init__(self, start, stop, delay=0.1):
        self.start = start
        self.stop = stop
        self.delay = delay

    def __aiter__(self):
        self.current = self.start
        return self

    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration

        await asyncio.sleep(self.delay)
        value = self.current
        self.current += 2
        return value


# 使用
async def main():
    print("异步迭代:")
    async for i in AsyncRange(0, 10, 0.2):
        print(f"  值: {i}")


asyncio.run(main())


# 八、异步生成器
# 异步生成器

async def async_generator(n):
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i * 2


# 使用
async def main():
    print("异步生成器:")
    async for value in async_generator(5):
        print(f"  生成值: {value}")


asyncio.run(main())
