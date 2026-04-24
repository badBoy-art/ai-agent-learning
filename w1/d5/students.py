from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Student:
    student_id: str
    name: str
    age: int
    grades: Dict[str, float]

    def add_grade(self, subject: str, grade: float) -> None:
        if 0 <= grade <= 100:
            self.grades[subject] = grade
        else:
            raise ValueError("成绩必须在0-100之间")

    def get_average(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def get_highest_grade(self) -> tuple:
        if not self.grades:
            return ("", 0)
        subject = max(self.grades, key=self.grades.get)
        return (subject, self.grades[subject])

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "grades": self.grades
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            grades=data.get("grades", {})
        )

    def __str__(self) -> str:
        avg = self.get_average()
        return f"学生({self.student_id}, {self.name}, 平均分: {avg:.1f})"
