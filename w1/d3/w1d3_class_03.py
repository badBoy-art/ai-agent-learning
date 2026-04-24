# 五、类属性和类方法
class Student:
    # 类属性 (所有对象共享)
    school = "清华大学"
    student_count = 0

    def __init__(self, name, grade):
        self.name = name  # 实例属性
        self.grade = grade
        Student.student_count += 1  # 修改类属性

    # 实例方法 (操作实例属性)
    def study(self):
        return f"{self.name}正在学习"

    # 类方法 (操作类属性)
    @classmethod
    def get_school(cls):
        return f"学校: {cls.school}"

    @classmethod
    def get_student_count(cls):
        return f"学生数量: {cls.student_count}"

    # 静态方法 (不需要访问实例或类属性)
    @staticmethod
    def is_passing_grade(grade):
        return grade >= 60


# 使用
s1 = Student("张三", 85)
s2 = Student("李四", 90)

print(Student.get_school())  # 学校: 清华大学
print(Student.get_student_count())  # 学生数量: 2
print(s1.study())  # 张三正在学习
print(Student.is_passing_grade(85))  # True

# 对比 Java:
# public class Student {
#     private static String school = "清华大学";
#     private String name;
#
#     public static String getSchool() { return school; }
#     public String study() { return name + "正在学习"; }
# }
