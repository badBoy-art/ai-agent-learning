students = {
    "001": {"name": "张三", "scores": {"语文": 90, "数学": 85, "英语": 92}},
    "002": {"name": "李四", "scores": {"语文": 88, "数学": 95, "英语": 78}},
    "003": {"name": "王五", "scores": {"语文": 92, "数学": 88, "英语": 90}}
}

# 计算每个学生的平均分
for sid, info in students.items():
    scores = info["scores"].values()
    avg = sum(scores) / len(scores)
    print(f"{sid} : {info['name']}的平均分: {avg:.1f}")

# 找出最高分的学生
best_student = max(students.items(),
                   key=lambda x: sum(x[1]["scores"].values()))
print(f"最高分学生: {best_student[1]['name']}")


# Lambda 是匿名函数
# 语法: lambda 参数: 表达式

# 等价写法:
# lambda x: sum(x[1]["scores"].values())

# 等价于:
def calculate_total(x):
    return sum(x[1]["scores"].values())


# 使用场景:
max(students.items(), key=calculate_total)


# 或者更清晰的写法:
def get_total_score(item):
    sid, info = item
    return sum(info["scores"].values())


best = max(students.items(), key=get_total_score)

evens = [x ** 2 for x in range(100) if x % 2 == 0]
print(f"偶数: {evens}")
