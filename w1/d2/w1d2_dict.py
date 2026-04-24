# Dict 字典 - 键值对存储
# 类似 Java 的 HashMap

# 1. 创建字典
person = {
    "name": "张三",
    "age": 25,
    "city": "北京",
    "hobbies": ["读书", "编程", "跑步"]
}

print(f"个人信息: {person}")

# 2. 访问值
print(f"姓名: {person['name']}")
print(f"年龄: {person.get('age')}")  # 安全访问
print(f"工资: {person.get('salary', 0)}")  # 不存在返回默认值
print(f"工资: {person.get('salary')}")  # 不存在返回None

# 3. 添加/修改
person['email'] = 'zhangsan@example.com'  # 添加新键
person['age'] = 26  # 修改值
print(f"更新后: {person}")

# 4. 删除
del person['email']  # 删除键
print(f"删除email后: {person}")

# 5. 字典方法
print(f"所有键: {list(person.keys())}")
print(f"所有值: {list(person.values())}")
print(f"所有项: {list(person.items())}")

# 6. 遍历字典
print("遍历字典:")
for key, value in person.items():
    print(f"  {key}: {value}")

# 7. 字典推导式
squares = {x: x ** 2 for x in range(5)}
print(f"平方字典: {squares}")

# 8. 嵌套字典
students = {
    "001": {"name": "张三", "score": 90},
    "002": {"name": "李四", "score": 85},
    "003": {"name": "王五", "score": 95}
}

print("学生信息:")
for sid, info in students.items():
    print(f"  {sid}: {info['name']} - {info['score']}分")
