# 九 特殊方法 (魔术方法)
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 字符串表示
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    # 加法运算符重载
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    # 减法运算符重载
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    # 乘法运算符重载
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    # 相等比较
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # 长度
    def __len__(self):
        return int((self.x ** 2 + self.y ** 2) ** 0.5)

    # 索引访问
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("索引只能是0或1")


# 使用
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1)  # Vector(3, 4)
print(v1 + v2)  # Vector(4, 6)
print(v1 - v2)  # Vector(2, 2)
print(v1 * 2)  # Vector(6, 8)
print(v1 == v2)  # False
print(len(v1))  # 5
print(v1[0])  # 3
print(v1[1])  # 4
