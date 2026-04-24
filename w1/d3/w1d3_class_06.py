# 八、封装
# Python 没有真正的私有属性，但有约定

class Employee:
    def __init__(self, name, salary):
        self.name = name  # 公有属性
        self._department = "IT"  # 保护属性 (约定，单下划线)
        self.__salary = salary  # 私有属性 (双下划线，名称改写)

    # Getter 方法
    def get_salary(self):
        return self.__salary

    # Setter 方法
    def set_salary(self, salary):
        if salary > 0:
            self.__salary = salary
        else:
            print("工资必须大于0")

    # 使用 property 装饰器 (更 Pythonic)
    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        if value > 0:
            self.__salary = value
        else:
            raise ValueError("工资必须大于0")


# 使用
emp = Employee("张三", 10000)

# 公有属性可以直接访问
print(emp.name)  # 张三

# 保护属性可以直接访问 (但不建议)
print(emp._department)  # IT

# 私有属性不能直接访问
# print(emp.__salary)  # AttributeError

# 通过方法访问
print(emp.get_salary())  # 10000
emp.set_salary(12000)
print(emp.get_salary())  # 12000

# 使用 property (更简洁)
print(emp.salary)  # 12000
emp.salary = 15000
print(emp.salary)  # 15000
