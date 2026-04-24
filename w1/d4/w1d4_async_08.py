# 十、实战: 异步文件操作
import aiofiles
import asyncio


# pip install aiofiles

async def read_file_async(filepath):
    """异步读取文件"""
    async with aiofiles.open(filepath, 'r', encoding='utf-8') as f:
        content = await f.read()
        return content


async def write_file_async(filepath, content):
    """异步写入文件"""
    async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
        await f.write(content)


async def process_files():
    """并发处理多个文件"""
    # 写入测试文件
    await write_file_async("/Users/admin/Desktop/PythonStudy/file/test1.txt", "这是文件1的内容")
    await write_file_async("/Users/admin/Desktop/PythonStudy/file/test2.txt", "这是文件2的内容")

    # 并发读取
    tasks = [
        read_file_async("/Users/admin/Desktop/PythonStudy/file/test1.txt"),
        read_file_async("/Users/admin/Desktop/PythonStudy/file/test2.txt")
    ]
    contents = await asyncio.gather(*tasks)

    print("文件内容:")
    for i, content in enumerate(contents):
        print(f"  文件{i + 1}: {content}")


asyncio.run(process_files())
