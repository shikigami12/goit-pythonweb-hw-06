
import random
from faker import Faker
from faker import Faker
from database import session
from models import Student, Group, Teacher, Subject, Grade

fake = Faker()

def generate_data():
    # Create groups
    groups = [Group(name=f'Group {i}') for i in range(1, 4)]
    session.add_all(groups)
    session.commit()

    # Create teachers
    teachers = [Teacher(fullname=fake.name()) for _ in range(random.randint(3, 5))]
    session.add_all(teachers)
    session.commit()

    # Create subjects
    subjects = [Subject(name=fake.catch_phrase(), teacher_id=random.choice(teachers).id) for _ in range(random.randint(5, 8))]
    session.add_all(subjects)
    session.commit()

    # Create students
    students = []
    for _ in range(random.randint(30, 50)):
        student = Student(
            fullname=fake.name(),
            group_id=random.choice(groups).id
        )
        students.append(student)
    session.add_all(students)
    session.commit()

    # Create grades
    for student in students:
        for _ in range(random.randint(1, 20)):
            grade = Grade(
                grade=random.randint(1, 100),
                date_of=fake.date_between(start_date='-1y', end_date='today'),
                student_id=student.id,
                subject_id=random.choice(subjects).id
            )
            session.add(grade)
    session.commit()

if __name__ == '__main__':
    generate_data()
    print("Database has been seeded with random data.")
    session.close()
