# 十、综合练习
# 练习1: 学生管理系统
class Student:
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grades = {}

    def add_grade(self, subject, grade):
        self.grades[subject] = grade

    def get_average(self):
        if not self.grades:
            return 0
        return sum(self.grades.values()) / len(self.grades)

    def __str__(self):
        avg = self.get_average()
        return f"学生({self.student_id}, {self.name}, 平均分: {avg:.1f})"


class StudentManager:
    def __init__(self):
        self.students = {}

    def add_student(self, student):
        self.students[student.student_id] = student

    def get_student(self, student_id):
        return self.students.get(student_id)

    def get_top_students(self, n=3):
        sorted_students = sorted(
            self.students.values(),
            key=lambda s: s.get_average(),
            reverse=True
        )
        return sorted_students[:n]


# 使用
manager = StudentManager()

s1 = Student("001", "张三", 20)
s1.add_grade("语文", 90)
s1.add_grade("数学", 85)

s2 = Student("002", "李四", 21)
s2.add_grade("语文", 88)
s2.add_grade("数学", 95)

s3 = Student("003", "王五", 20)
s3.add_grade("语文", 92)
s3.add_grade("数学", 88)

manager.add_student(s1)
manager.add_student(s2)
manager.add_student(s3)

print("所有学生:")
for s in manager.students.values():
    print(f"  {s}")

print("\n前2名学生:")
for s in manager.get_top_students(2):
    print(f"  {s}")
