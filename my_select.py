import sqlalchemy
from sqlalchemy import func, desc, select, and_, cast, Numeric

from models import Student, Group, Teacher, Subject, Grade
from session import get_db

session = next(get_db())

def select_01():
    '''Знайти 5 студентів із найбільшим середнім балом з усіх предметів.'''
    result = session.query(
        Student.id, 
        Student.name, 
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    
    # Post-process the results to round the average_grade to 2 decimal places
    rounded_result = [
        (student_id, name, round(average_grade, 2))
        for student_id, name, average_grade in result
    ]
    
    return rounded_result

def select_02():
    '''Знайти студента із найвищим середнім балом з певного предмета.'''
    subject_id = 1  # Замініть на потрібний ідентифікатор предмета
    result = session.query(
        Student.id, 
        Student.name, 
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).filter(Grade.subject_id == subject_id).group_by(Student.id).order_by(desc('average_grade')).limit(1).all()
    
    # Post-process the result to round the average_grade to 2 decimal places
    rounded_result = [
        (student_id, name, round(average_grade, 2))
        for student_id, name, average_grade in result
    ]
    
    return rounded_result

def select_03(subject_id='1'):
    '''Знайти середній бал у групах з певного предмета.'''
    result = session.query(
        Group.id.label('group_id'),
        Group.name.label('group_name'),
        func.cast(func.avg(Grade.grade), sqlalchemy.types.Numeric(10, 2)).label('average_grade')
    ).join(Student, Student.group_id == Group.id).join(Grade, Grade.student_id == Student.id).filter(
        Grade.subject_id == subject_id
    ).group_by(Group.id).order_by(Group.id).all()
    
    return result

def select_04():
    '''Знайти середній бал на потоці (по всій таблиці оцінок).'''
    result = session.query(cast(func.avg(Grade.grade), Numeric(10, 2)).label('average_grade')).all()
    
    return result

def select_05(teacher_name = "Lisa Johnson"):
    '''Знайти які курси читає певний викладач.'''
    result = session.query(Subject.name)\
                    .join(Subject.teacher)\
                    .filter(Teacher.name == teacher_name)\
                    .all()
    return result


def select_06(group_name = "Group 1"):
    '''Знайти список студентів у певній групі.'''
    result = session.query(Student.name)\
                    .join(Student.group)\
                    .filter(Group.name == group_name)\
                    .all()
    return result

def select_07(group_name='Group 2', subject_name = 'it'):
    '''Знайти оцінки студентів у окремій групі з певного предмета.'''
    result = session.query(Grade.grade)\
                    .join(Grade.student)\
                    .join(Student.group)\
                    .join(Grade.subject)\
                    .filter(Group.name == group_name)\
                    .filter(Subject.name == subject_name)\
                    .all()
    return result
def select_08(teacher_name = 'Scott Carroll'):
    '''Знайти середній бал, який ставить певний викладач зі своїх предметів.'''
    result = session.query(func.avg(Grade.grade).label('average_grade'))\
                    .join(Grade.subject)\
                    .join(Subject.teacher)\
                    .filter(Teacher.name == teacher_name)\
                    .group_by(Teacher.id)\
                    .first()
    return result[0] if result else None

def select_09(student_id = '1'):
    '''Знайти список курсів, які відвідує певний студент.'''
    result = session.query(Subject.name)\
                    .join(Grade.subject)\
                    .join(Grade.student)\
                    .filter(Student.id == student_id)\
                    .distinct()\
                    .all()
    return [course[0] for course in result] if result else None

def select_10(student_id='1', teacher_id='1'):
    '''Список курсів, які певному студенту читає певний викладач.'''
    result = session.query(Subject.name)\
                    .join(Grade.subject)\
                    .join(Grade.student)\
                    .join(Subject.teacher)\
                    .filter(and_(Student.id == student_id, Teacher.id == teacher_id))\
                    .distinct()\
                    .all()
    return [course[0] for course in result] if result else None

if __name__ == "__main__":
   
    # print(f"select'1' : {select_01()}")

    # print(f"select'2' : {select_02()}")

    # results = select_03()
    # for res in results:
    #     print(f"Group ID: {res.group_id}, Group Name: {res.group_name}, Average Grade: {res.average_grade}")
    
    # average_grade = select_04()
    # if average_grade:
    #     print(f"Average Grade: {average_grade[0].average_grade}")
    # else:
    #     print("No data found")
    # print(f"select'5' : {select_05()}")
    # print(f"select'6' : {select_06()}")
    # print(f"select'7' : {select_07()}")
    # print(f"select'8' : {select_08()}")
    # print(f"select'9' : {select_09()}")
    # print(f"select'10' : {select_10()}")
    