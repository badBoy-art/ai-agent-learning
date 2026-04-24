# 1. 变量和数据类型
name = "张三"
age = 25
height = 1.75
is_student = True
print(f"姓名: {name}")
print(f"年龄: {age}")

# 列表 (类似 Java 的 ArrayList)
fruits = ["苹果", "香蕉", "橙子"]
print(f"水果: {fruits}")
fruits.append("葡萄")
print(f"水果 append: {fruits}")

# 字典(类似 Java 的 HashMap)
person = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}
print(f"姓名: {person['name']}")

# 4. 条件语句
score = 85
if score >= 90:
    print("优秀")
elif score >= 80:
    print("良好")
else:
    print("及格")

# 5. 循环
for fruit in fruits:
    print(f"水果: {fruit}")


# 6. 函数
def greet(name):
    return f"你好, {name}!"


print(greet("张三"))


# 7. 类
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"我叫{self.name}，今年{self.age}岁"


person = Person("张三", 25)
print(person.introduce())
