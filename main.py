
import argparse
from datetime import datetime

from sqlalchemy.exc import IntegrityError

from database import session
from models import Teacher, Group, Student, Subject, Grade

# --- Teacher CRUD --- #
def create_teacher(name):
    teacher = Teacher(fullname=name)
    session.add(teacher)
    session.commit()
    print(f"Teacher '{name}' created with ID {teacher.id}")

def list_teachers():
    teachers = session.query(Teacher).all()
    for t in teachers:
        print(f"ID: {t.id}, Name: {t.fullname}")

def update_teacher(teacher_id, new_name):
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    if teacher:
        teacher.fullname = new_name
        session.commit()
        print(f"Teacher {teacher_id} updated to '{new_name}'")
    else:
        print(f"Teacher with ID {teacher_id} not found.")

def remove_teacher(teacher_id):
    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    if teacher:
        session.delete(teacher)
        session.commit()
        print(f"Teacher {teacher_id} removed.")
    else:
        print(f"Teacher with ID {teacher_id} not found.")

# --- Group CRUD --- #
def create_group(name):
    group = Group(name=name)
    session.add(group)
    session.commit()
    print(f"Group '{name}' created with ID {group.id}")

def list_groups():
    groups = session.query(Group).all()
    for g in groups:
        print(f"ID: {g.id}, Name: {g.name}")

def update_group(group_id, new_name):
    group = session.query(Group).filter_by(id=group_id).first()
    if group:
        group.name = new_name
        session.commit()
        print(f"Group {group_id} updated to '{new_name}'")
    else:
        print(f"Group with ID {group_id} not found.")

def remove_group(group_id):
    group = session.query(Group).filter_by(id=group_id).first()
    if group:
        session.delete(group)
        session.commit()
        print(f"Group {group_id} removed.")
    else:
        print(f"Group with ID {group_id} not found.")

# --- Student CRUD --- #
def create_student(fullname, group_id):
    student = Student(fullname=fullname, group_id=group_id)
    session.add(student)
    session.commit()
    print(f"Student '{fullname}' created in group {group_id}")

def list_students():
    students = session.query(Student).all()
    for s in students:
        print(f"ID: {s.id}, Name: {s.fullname}, Group ID: {s.group_id}")

def update_student(student_id, new_fullname=None, new_group_id=None):
    student = session.query(Student).filter_by(id=student_id).first()
    if student:
        if new_fullname:
            student.fullname = new_fullname
        if new_group_id:
            student.group_id = new_group_id
        session.commit()
        print(f"Student {student_id} updated.")
    else:
        print(f"Student with ID {student_id} not found.")

def remove_student(student_id):
    student = session.query(Student).filter_by(id=student_id).first()
    if student:
        session.delete(student)
        session.commit()
        print(f"Student {student_id} removed.")
    else:
        print(f"Student with ID {student_id} not found.")

# --- Subject CRUD --- #
def create_subject(name, teacher_id):
    subject = Subject(name=name, teacher_id=teacher_id)
    session.add(subject)
    session.commit()
    print(f"Subject '{name}' created for teacher {teacher_id}")

def list_subjects():
    subjects = session.query(Subject).all()
    for s in subjects:
        print(f"ID: {s.id}, Name: {s.name}, Teacher ID: {s.teacher_id}")

def update_subject(subject_id, new_name=None, new_teacher_id=None):
    subject = session.query(Subject).filter_by(id=subject_id).first()
    if subject:
        if new_name:
            subject.name = new_name
        if new_teacher_id:
            subject.teacher_id = new_teacher_id
        session.commit()
        print(f"Subject {subject_id} updated.")
    else:
        print(f"Subject with ID {subject_id} not found.")

def remove_subject(subject_id):
    subject = session.query(Subject).filter_by(id=subject_id).first()
    if subject:
        session.delete(subject)
        session.commit()
        print(f"Subject {subject_id} removed.")
    else:
        print(f"Subject with ID {subject_id} not found.")

# --- Grade CRUD --- #
def create_grade(grade, date_of, student_id, subject_id):
    date_obj = datetime.strptime(date_of, '%Y-%m-%d').date()
    grade_obj = Grade(grade=grade, date_of=date_obj, student_id=student_id, subject_id=subject_id)
    session.add(grade_obj)
    session.commit()
    print(f"Grade {grade} created for student {student_id} in subject {subject_id}")

def list_grades():
    grades = session.query(Grade).all()
    for g in grades:
        print(f"ID: {g.id}, Grade: {g.grade}, Date: {g.date_of}, Student ID: {g.student_id}, Subject ID: {g.subject_id}")

def update_grade(grade_id, new_grade=None, new_date_of=None):
    grade = session.query(Grade).filter_by(id=grade_id).first()
    if grade:
        if new_grade:
            grade.grade = new_grade
        if new_date_of:
            grade.date_of = datetime.strptime(new_date_of, '%Y-%m-%d').date()
        session.commit()
        print(f"Grade {grade_id} updated.")
    else:
        print(f"Grade with ID {grade_id} not found.")

def remove_grade(grade_id):
    grade = session.query(Grade).filter_by(id=grade_id).first()
    if grade:
        session.delete(grade)
        session.commit()
        print(f"Grade {grade_id} removed.")
    else:
        print(f"Grade with ID {grade_id} not found.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI for CRUD operations on the database.')
    parser.add_argument('-a', '--action', required=True, choices=['create', 'list', 'update', 'remove'], help='Action to perform')
    parser.add_argument('-m', '--model', required=True, choices=['Teacher', 'Group', 'Student', 'Subject', 'Grade'], help='Model to interact with')
    
    # Common arguments
    parser.add_argument('--id', type=int, help='ID of the record')
    parser.add_argument('-n', '--name', type=str, help='Name, title, or full name for a record')

    # Model-specific arguments
    parser.add_argument('--group_id', type=int, help='Group ID')
    parser.add_argument('--teacher_id', type=int, help='Teacher ID')
    parser.add_argument('--student_id', type=int, help='Student ID')
    parser.add_argument('--subject_id', type=int, help='Subject ID')
    parser.add_argument('--grade', type=int, help='Grade value')
    parser.add_argument('--date_of', type=str, help='Date in YYYY-MM-DD format')

    args = parser.parse_args()

    try:
        if args.model == 'Teacher':
            if args.action == 'create':
                create_teacher(args.name)
            elif args.action == 'list':
                list_teachers()
            elif args.action == 'update':
                update_teacher(args.id, args.name)
            elif args.action == 'remove':
                remove_teacher(args.id)

        elif args.model == 'Group':
            if args.action == 'create':
                create_group(args.name)
            elif args.action == 'list':
                list_groups()
            elif args.action == 'update':
                update_group(args.id, args.name)
            elif args.action == 'remove':
                remove_group(args.id)

        elif args.model == 'Student':
            if args.action == 'create':
                create_student(args.name, args.group_id)
            elif args.action == 'list':
                list_students()
            elif args.action == 'update':
                update_student(args.id, new_fullname=args.name, new_group_id=args.group_id)
            elif args.action == 'remove':
                remove_student(args.id)

        elif args.model == 'Subject':
            if args.action == 'create':
                create_subject(args.name, args.teacher_id)
            elif args.action == 'list':
                list_subjects()
            elif args.action == 'update':
                update_subject(args.id, new_name=args.name, new_teacher_id=args.teacher_id)
            elif args.action == 'remove':
                remove_subject(args.id)

        elif args.model == 'Grade':
            if args.action == 'create':
                create_grade(args.grade, args.date_of, args.student_id, args.subject_id)
            elif args.action == 'list':
                list_grades()
            elif args.action == 'update':
                update_grade(args.id, new_grade=args.grade, new_date_of=args.date_of)
            elif args.action == 'remove':
                remove_grade(args.id)

    except IntegrityError as e:
        session.rollback()
        print(f"Database Integrity Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()
