
import sys
import codecs

# Fix for UnicodeEncodeError on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from sqlalchemy import func, desc

from database import session
from models import Student, Group, Teacher, Subject, Grade

def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    print("--- Query 1: 5 студентів із найбільшим середнім балом ---")
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    print(result)

def select_2(subject_id=1):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    print(f"--- Query 2: Студент із найвищим середнім балом з предмета ID={subject_id} ---")
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subject_id == subject_id) \
        .group_by(Student.id).order_by(desc('avg_grade')).first()
    print(result)

def select_3(subject_id=1):
    """Знайти середній бал у групах з певного предмета."""
    print(f"--- Query 3: Середній бал у групах з предмета ID={subject_id} ---")
    result = session.query(Group.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).join(Group).filter(Grade.subject_id == subject_id) \
        .group_by(Group.id).order_by(desc('avg_grade')).all()
    print(result)

def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    print("--- Query 4: Середній бал на потоці ---")
    result = session.query(func.round(func.avg(Grade.grade), 2)).scalar()
    print(result)

def select_5(teacher_id=1):
    """Знайти які курси читає певний викладач."""
    print(f"--- Query 5: Курси, які читає викладач ID={teacher_id} ---")
    result = session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
    print([r[0] for r in result])

def select_6(group_id=1):
    """Знайти список студентів у певній групі."""
    print(f"--- Query 6: Список студентів у групі ID={group_id} ---")
    result = session.query(Student.fullname).filter(Student.group_id == group_id).all()
    print([r[0] for r in result])

def select_7(group_id=1, subject_id=1):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    print(f"--- Query 7: Оцінки студентів групи ID={group_id} з предмета ID={subject_id} ---")
    result = session.query(Student.fullname, Grade.grade, Grade.date_of) \
        .select_from(Grade).join(Student) \
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()
    print(result)

def select_8(teacher_id=1):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    print(f"--- Query 8: Середній бал, який ставить викладач ID={teacher_id} ---")
    result = session.query(func.round(func.avg(Grade.grade), 2)) \
        .select_from(Grade).join(Subject).filter(Subject.teacher_id == teacher_id).scalar()
    print(result)

def select_9(student_id=1):
    """Знайти список курсів, які відвідує певний студент."""
    print(f"--- Query 9: Список курсів студента ID={student_id} ---")
    result = session.query(func.distinct(Subject.name)) \
        .select_from(Grade).join(Subject).filter(Grade.student_id == student_id).all()
    print([r[0] for r in result])

def select_10(student_id=1, teacher_id=1):
    """Список курсів, які певному студенту читає певний викладач."""
    print(f"--- Query 10: Курси студента ID={student_id}, які читає викладач ID={teacher_id} ---")
    result = session.query(func.distinct(Subject.name)) \
        .select_from(Grade).join(Subject) \
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id).all()
    print([r[0] for r in result])

def select_11(student_id=1, teacher_id=1):
    """Середній бал, який певний викладач ставить певному студентові."""
    print(f"--- Query 11: Середній бал студента ID={student_id} від викладача ID={teacher_id} ---")
    result = session.query(func.round(func.avg(Grade.grade), 2)) \
        .select_from(Grade) \
        .join(Subject) \
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id) \
        .scalar()
    print(result)

def select_12(group_id=1, subject_id=1):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""
    print(f"--- Query 12: Оцінки групи ID={group_id} з предмета ID={subject_id} на останньому занятті ---")
    
    subquery = session.query(func.max(Grade.date_of)) \
        .join(Student) \
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id) \
        .scalar_subquery()

    result = session.query(Student.fullname, Grade.grade, Grade.date_of) \
        .join(Grade) \
        .filter(
            Student.group_id == group_id, 
            Grade.subject_id == subject_id,
            Grade.date_of == subquery
        ).all()
    
    print(result)

if __name__ == '__main__':
    select_1()
    select_2()
    select_3()
    select_4()
    select_5()
    select_6()
    select_7()
    select_8()
    select_9()
    select_10()
    # --- Additional queries ---
    select_11(student_id=1, teacher_id=1)
    select_12(group_id=1, subject_id=1)
    session.close()
