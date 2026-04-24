# 六、继承
# 父类 (基类)
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        return f"{self.name}正在吃东西"

    def sleep(self):
        return f"{self.name}正在睡觉"

    def speak(self):
        return f"{self.name}发出声音"


# 子类 (派生类)
class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)  # 调用父类构造函数
        self.breed = breed

    # 重写父类方法
    def speak(self):
        return f"{self.name}汪汪叫"

    # 子类特有方法
    def fetch(self):
        return f"{self.name}在捡球"


class Cat(Animal):
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color

    def speak(self):
        return f"{self.name}喵喵叫"

    def climb(self):
        return f"{self.name}在爬树"


# 使用
dog = Dog("旺财", 3, "金毛")
cat = Cat("咪咪", 2, "橘色")

print(dog.eat())  # 旺财正在吃东西 (继承自父类)
print(dog.speak())  # 旺财汪汪叫 (重写)
print(dog.fetch())  # 旺财在捡球 (子类特有)

print(cat.eat())  # 咪咪正在吃东西
print(cat.speak())  # 咪咪喵喵叫
print(cat.climb())  # 咪咪在爬树

# Java 对比:
# public class Dog extends Animal {
#     private String breed;
#
#     public Dog(String name, int age, String breed) {
#         super(name, age);
#         this.breed = breed;
#     }
#
#     @Override
#     public String speak() {
#         return name + "汪汪叫";
#     }
# }
