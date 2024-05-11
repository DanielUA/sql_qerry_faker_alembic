from faker import Faker
from sqlalchemy.orm import Session
from models import Student, Group, Teacher, Subject, Grade
import random
from datetime import datetime, timedelta

faker = Faker()

def fill_data(session: Session):
    # Створення груп
    groups = [Group(name=f"Group {i}") for i in range(1, 4)]
    session.add_all(groups)

    # Створення викладачів
    teachers = [Teacher(name=faker.name()) for _ in range(3, 6)]  # Від 3 до 5 викладачів
    session.add_all(teachers)

    # Створення предметів
    subjects = [Subject(name=faker.word(), teacher=random.choice(teachers)) for _ in range(5, 9)]  # 5-8 предметів
    session.add_all(subjects)

    # Створення студентів
    students = [Student(name=faker.name(), group=random.choice(groups)) for _ in range(30, 51)]  # 30-50 студентів
    session.add_all(students)

    # Створення оцінок для студентів
    for student in students:
        for _ in range(random.randint(10, 20)):  # До 20 оцінок для кожного студента
            subject = random.choice(subjects)
            grade = random.uniform(1.0, 100.0)  # Випадкові оцінки
            date_received = datetime.utcnow() - timedelta(days=random.randint(1, 365))  # Випадкова дата
            new_grade = Grade(student=student, subject=subject, grade=grade, date_received=date_received)
            session.add(new_grade)

    session.commit()  # Збереження змін

if __name__ == "__main__":
    fill_data()