import json
from dataclasses import dataclass
from typing import List, Dict, Optional
from students import Student  # 修复导入语法


class StudentManager:
    def __init__(self):
        self.students: Dict[str, Student] = {}

    def add_student(self, student: Student) -> None:
        if student.student_id in self.students:
            raise ValueError(f"学号 {student.student_id} 已存在")
        self.students[student.student_id] = student
        print(f"添加学生: {student.name}")

    def remove_student(self, student_id: str) -> Optional[Student]:
        if student_id not in self.students:
            raise ValueError(f"学号 {student_id} 不存在")
        student = self.students.pop(student_id)
        print(f"删除学生: {student.name}")
        return student

    def get_student(self, student_id: str) -> Optional[Student]:
        return self.students.get(student_id)

    def get_all_students(self) -> List[Student]:
        return list(self.students.values())

    def get_top_students(self, n: int = 3) -> List[Student]:
        sorted_students = sorted(
            self.students.values(),
            key=lambda s: s.get_average(),
            reverse=True
        )
        return sorted_students[:n]

    def get_class_average(self) -> float:
        if not self.students:
            return 0.0
        total = sum(s.get_average() for s in self.students.values())
        return total / len(self.students)

    def save_to_file(self, filepath: str) -> None:
        data = {
            "students": [s.to_dict() for s in self.students.values()]
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"保存到: {filepath}")

    def load_from_file(self, filepath: str) -> None:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.students.clear()
        for student_data in data.get("students", []):
            student = Student.from_dict(student_data)
            self.students[student.student_id] = student
        print(f"从 {filepath} 加载了 {len(self.students)} 个学生")

    def __str__(self) -> str:
        return f"学生管理器(共 {len(self.students)} 名学生)"
