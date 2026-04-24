# 七、多态
# 多态: 不同对象对同一消息做出不同响应

class Shape:
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height


# 多态的体现
shapes = [
    Circle(5),
    Rectangle(4, 6),
    Triangle(3, 8)
]

print("计算各种形状的面积:")
for shape in shapes:
    # 同样调用 area()，但结果不同
    print(f"  {shape.__class__.__name__}: {shape.area():.2f}")
