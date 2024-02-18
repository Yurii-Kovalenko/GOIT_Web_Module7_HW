from sqlalchemy import create_engine, select, func, desc

from sqlalchemy.orm import sessionmaker

from models import DB_URL

from models import Group, Student, Lector, Subject, Mark

from auxiliary_functions import input_in_range

from choice_of import (
    choice_of_subject,
    choice_of_student,
    choice_of_lector,
    choice_of_group,
)


def select_1() -> list[tuple]:
    rules_of_select = (
        select(Student.name, func.avg(Mark.value).label("AverageMarks"))
        .select_from(Mark)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("AverageMarks"))
        .limit(5)
    )
    result = session.execute(rules_of_select).all()
    return result


def select_2() -> list[tuple]:
    subject_name = choice_of_subject()[1]
    rules_of_select = (
        select(
            func.avg(Mark.value).label("AverageMarks"),
            Student.name.label("Student"),
            Subject.name.label("Subject"),
        )
        .select_from(Mark)
        .join(Student)
        .join(Subject)
        .where(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(desc("AverageMarks"))
        .limit(1)
    )
    result = session.execute(rules_of_select).all()
    return result


def select_3() -> list[tuple]:
    subject_name = choice_of_subject()[1]
    rules_of_select = (
        select(
            func.avg(Mark.value).label("AverageMarks"),
            Group.name.label("Group_name"),
            Subject.name.label("Subject"),
        )
        .select_from(Mark)
        .join(Student)
        .join(Subject)
        .join(Group)
        .where(Subject.name == subject_name)
        .group_by(Group.id)
        .order_by(Group.name)
    )
    result = session.execute(rules_of_select).all()
    return result


def select_4() -> list[tuple]:
    rules_of_select = select(func.avg(Mark.value).label("AverageMarks")).select_from(
        Mark
    )
    result = session.execute(rules_of_select).all()
    return result


def select_5() -> list[tuple]:
    lector_name = choice_of_lector()[1]
    rules_of_select = (
        select(Subject.name.label("Subject"), Lector.name.label("Lector"))
        .select_from(Subject)
        .join(Lector)
        .where(Lector.name == lector_name)
        .order_by(Subject.name)
    )
    result = session.execute(rules_of_select).all()
    return result


def select_6() -> list[tuple]:
    group_name = choice_of_group()[1]
    rules_of_select = (
        select(Student.name.label("Student"), Group.name.label("Group_name"))
        .select_from(Student)
        .join(Group)
        .where(Group.name == group_name)
        .order_by(Student.name)
    )
    result = session.execute(rules_of_select).all()
    return result


def select_7() -> list[tuple]:
    group_name = choice_of_group()[1]
    subject_name = choice_of_subject()[1]
    rules_of_select = (
        select(
            Student.name.label("Student"),
            Mark.value.label("Mark"),
            Mark.date_of.label("Date"),
            Subject.name.label("Subject"),
            Group.name.label("Group_name"),
        )
        .select_from(Mark)
        .join(Student)
        .join(Subject)
        .join(Group)
        .where(Group.name == group_name)
        .where(Subject.name == subject_name)
        .order_by(Student.name)
    )
    result = session.execute(rules_of_select).all()
    return result


def select_8() -> list[tuple]:
    lector_name = choice_of_lector()[1]
    rules_of_select = (
        select(
            func.avg(Mark.value).label("AverageMarks"),
            Subject.name.label("Subject"),
            Lector.name.label("Lector"),
        )
        .select_from(Mark)
        .join(Subject)
        .join(Lector)
        .where(Lector.name == lector_name)
        .group_by(Subject.id)
        .order_by(Subject.name)
    )
    result = session.execute(rules_of_select).all()
    return result


def select_9() -> list[tuple]:
    student_name = choice_of_student()[1]
    rules_of_select = (
        select(Student.name.label("Student"), Subject.name.label("Subject"))
        .select_from(Subject)
        .join(Mark)
        .join(Student)
        .where(Student.name == student_name)
        .order_by(Subject.name)
        .distinct()
    )
    result = session.execute(rules_of_select).all()
    return result


def select_10() -> list[tuple]:
    student_name = choice_of_student()[1]
    lector_name = choice_of_lector()[1]
    rules_of_select = (
        select(
            Student.name.label("Student"),
            Subject.name.label("Subject"),
            Lector.name.label("Lector"),
        )
        .select_from(Subject)
        .join(Mark)
        .join(Lector)
        .join(Student)
        .where(Student.name == student_name)
        .where(Lector.name == lector_name)
        .order_by(Subject.name)
        .distinct()
    )
    result = session.execute(rules_of_select).all()
    return result


def select_11() -> list[tuple]:
    student_name = choice_of_student()[1]
    lector_name = choice_of_lector()[1]
    rules_of_select = (
        select(
            func.avg(Mark.value).label("AverageMarks"),
            Student.name.label("Student"),
            Lector.name.label("Lector"),
        )
        .select_from(Mark)
        .join(Subject)
        .join(Lector)
        .join(Student)
        .where(Student.name == student_name)
        .where(Lector.name == lector_name)
    )
    result = session.execute(rules_of_select).all()
    return result


def select_12() -> list[tuple]:
    group_name = choice_of_group()[1]
    subject_name = choice_of_subject()[1]
    rules_of_subselect = (
        select(func.max(Mark.date_of))
        .select_from(Mark)
        .join(Student)
        .join(Subject)
        .join(Group)
        .where(Group.name == group_name)
        .where(Subject.name == subject_name)
    )
    rules_of_select = (
        select(Student.name, Mark.value, Mark.date_of, Subject.name, Group.name)
        .select_from(Mark)
        .join(Student)
        .join(Subject)
        .join(Group)
        .where(Group.name == group_name)
        .where(Subject.name == subject_name)
        .where(Mark.date_of == rules_of_subselect.scalar_subquery())
        .order_by(Student.name)
    )
    result = session.execute(rules_of_select).all()
    return result


func_of_select = {}
func_of_select[1] = select_1
func_of_select[2] = select_2
func_of_select[3] = select_3
func_of_select[4] = select_4
func_of_select[5] = select_5
func_of_select[6] = select_6
func_of_select[7] = select_7
func_of_select[8] = select_8
func_of_select[9] = select_9
func_of_select[10] = select_10
func_of_select[11] = select_11
func_of_select[12] = select_12


def execute_select(select_number: int) -> list[tuple]:
    return func_of_select.get(select_number)()


if __name__ == "__main__":
    engine = create_engine(DB_URL, echo=False)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    select_number = input_in_range("Enter the select number", 1, 12)
    print(execute_select(select_number))
