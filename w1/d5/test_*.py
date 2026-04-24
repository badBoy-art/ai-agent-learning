# 测试代码
import asyncio

from students import Student  # 修复导入语法
from student_manager import StudentManager
from w1.d5.library import Library, Book, Member
from w1.d5.task_scheduler import AsyncTaskScheduler, AsyncTask
from web_crawler import AsyncWebCrawler


def test_student_manager():
    print("=== 学生管理系统测试 ===\n")

    # 创建管理器
    manager = StudentManager()

    # 添加学生
    s1 = Student("001", "张三", 20, {"语文": 90, "数学": 85})
    s2 = Student("002", "李四", 21, {"语文": 88, "数学": 95})
    s3 = Student("003", "王五", 20, {"语文": 92, "数学": 88})

    manager.add_student(s1)
    manager.add_student(s2)
    manager.add_student(s3)

    # 添加成绩
    s1.add_grade("英语", 92)
    s2.add_grade("英语", 78)
    s3.add_grade("英语", 90)

    # 查询
    print(f"\n所有学生:")
    for s in manager.get_all_students():
        print(f"  {s}")

    print(f"\n班级平均分: {manager.get_class_average():.1f}")

    print(f"\n前2名:")
    for s in manager.get_top_students(2):
        print(f"  {s}")

    # 保存和加载
    manager.save_to_file("students.json")

    # 测试删除
    manager.remove_student("002")
    print(f"\n删除后:")
    for s in manager.get_all_students():
        print(f"  {s}")


test_student_manager()


# 测试爬虫
async def test_web_crawler():
    print("=== 异步爬虫测试 ===\n")

    urls = [
        "https://httpbin.org",
        "https://example.com",
        "https://httpbin.org/get"
    ]

    crawler = AsyncWebCrawler(timeout=10.0, max_concurrent=3)
    pages = await crawler.crawl(urls)

    print(f"\n爬取结果:")
    for page in pages:
        print(f"  URL: {page.url}")
        print(f"  状态: {page.status_code}")
        print(f"  标题: {page.title}")
        print(f"  链接数: {len(page.links)}")
        print(f"  词数: {page.word_count}")
        print()

    stats = crawler.get_statistics()
    print(f"统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    crawler.save_results("crawl_results.json")


asyncio.run(test_web_crawler())


# 图书
def test_library():
    print("=== 图书管理系统测试 ===\n")

    # 创建图书馆
    library = Library("城市图书馆")

    # 添加图书
    library.add_book(Book("978-7-111-11111-1", "Python编程", "张三", "编程"))
    library.add_book(Book("978-7-111-11111-2", "Java编程", "李四", "编程"))
    library.add_book(Book("978-7-111-11111-3", "数据结构", "王五", "计算机"))
    library.add_book(Book("978-7-111-11111-4", "红楼梦", "曹雪芹", "文学"))

    # 添加会员
    library.add_member(Member("M001", "小明"))
    library.add_member(Member("M002", "小红"))

    # 借书
    library.borrow_book("978-7-111-11111-1", "M001")
    library.borrow_book("978-7-111-11111-2", "M001")

    # 查询
    print(f"\n搜索'编程':")
    for book in library.search_books("编程"):
        print(f"  {book}")

    print(f"\n可借图书:")
    for book in library.get_available_books():
        print(f"  {book}")

    print(f"\n统计信息:")
    stats = library.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # 保存
    library.save_to_file("library.json")


test_library()


# 测试异步代码
async def test_task_scheduler():
    print("=== 异步任务调度器测试 ===\n")

    # 定义任务函数
    async def fetch_data(source: str):
        await asyncio.sleep(1)
        return f"数据来自 {source}"

    async def process_data(data: str):
        await asyncio.sleep(0.5)
        return f"处理完成: {data}"

    async def save_result(result: str):
        await asyncio.sleep(0.3)
        print(f"保存结果: {result}")
        return "已保存"

    # 创建调度器
    scheduler = AsyncTaskScheduler(max_concurrent=3)

    # 添加任务
    scheduler.add_task(AsyncTask("fetch", fetch_data, "API", max_retries=2))
    scheduler.add_task(AsyncTask("process", process_data, "原始数据",
                                 dependencies=["fetch"]))
    scheduler.add_task(AsyncTask("save", save_result, "处理结果",
                                 dependencies=["process"]))

    # 运行所有任务
    results = await scheduler.run_all()

    # 打印结果
    print(f"\n任务结果:")
    for task_id, result in results.items():
        print(f"  {task_id}: {result.status.value}")
        if result.result:
            print(f"    结果: {result.result}")

    print(f"\n统计信息:")
    stats = scheduler.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")


asyncio.run(test_task_scheduler())
