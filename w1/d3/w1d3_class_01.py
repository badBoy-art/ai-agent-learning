# 1. 定义一个简单的类
class Person:
    pass  # 空类


# 2. 创建对象
p = Person()
print(type(p))
# 3. 添加属性
p.name = "张三"
p.age = 25
print(p.name)  # 张三
print(p.age)  # 25


# 4. 定义带方法的类
class Person:
    def say_hello(self):  # Python 的方法第一个参数必须是 self
        print("你好，我是一个人")


p = Person()
p.say_hello()  # 你好，我是一个人


# 三、构造函数 __init__
# __init__ 是构造函数，创建对象时自动调用
class Person:
    def __init__(self, name, age):
        self.name = name  # 实例属性
        self.age = age

    def introduce(self):
        return f"我叫{self.name}，今年{self.age}岁"


p1 = Person("zhangsan", 15);
p2 = Person("lisi", 20);
print(p1.introduce())
print(p2.introduce())
