from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from models import DB_URL

from models import Group, Student, Lector, Subject, Mark

from faker import Faker

from random import randint

from datetime import date

from datetime import timedelta


NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = 8
NUMBER_LECTORS = 5
NUMBER_MARKS = (15, 20)

MARKS_RANGE = (2, 12)

START_DATE = date(2024, 1, 8)


GROUPS = ["IT-25", "PM-45", "MC-12"]

SUBJECTS = [
    "Math",
    "History",
    "Ukrainian",
    "English",
    "Astronomy",
    "Physics",
    "Chemistry",
    "Literature",
]


def fake_names(number: int) -> list[str]:
    fake_class = Faker()
    return [fake_class.name() for _ in range(number)]


def fake_names_ids(number: int, range_of_ids: int) -> list[tuple[str, int]]:
    fake_list = []
    fake_class = Faker()
    for _ in range(number):
        fake_list.append((fake_class.name(), randint(1, range_of_ids)))
    return fake_list


def subjects_and_ids(number: int, range_of_ids: int) -> list[tuple[str, int]]:
    while True:
        ids = set()
        fake_list = []
        for i in range(number):
            id_of_lector = randint(1, range_of_ids)
            ids.add(id_of_lector)
            fake_list.append((SUBJECTS[i], id_of_lector))
        if len(ids) == range_of_ids:
            break
    return fake_list


def fill_table_groups() -> None:
    for name_group in GROUPS:
        session.add(Group(name=name_group))
    session.commit()


def fill_table_students() -> list[tuple[str, int]]:
    my_students = fake_names_ids(NUMBER_STUDENTS, NUMBER_GROUPS)
    for student_info in my_students:
        session.add(Student(name=student_info[0], group_id_fn=student_info[1]))
    session.commit()
    return my_students


def fill_table_lectors() -> None:
    my_lectors = fake_names(NUMBER_LECTORS)
    for name_lector in my_lectors:
        session.add(Lector(name=name_lector))
    session.commit()


def fill_table_subjects() -> None:
    my_subjects = subjects_and_ids(NUMBER_SUBJECTS, NUMBER_LECTORS)
    for subject_info in my_subjects:
        session.add(Subject(name=subject_info[0], lector_id_fn=subject_info[1]))
    session.commit()


def find_numer_of_marks_by_students(
    my_students: list[tuple[str, int]]
) -> dict[int:int]:
    result = dict()
    id_student = 0
    for _ in my_students:
        id_student += 1
        result[id_student] = randint(*NUMBER_MARKS)
    return result


def find_group_by_students(my_students: list[tuple[str, int]]) -> dict[int:int]:
    result = dict()
    id_student = 0
    for student_info in my_students:
        id_student += 1
        result[id_student] = student_info[1]
    return result


def fill_table_marks(my_students: list[tuple[str, int]]) -> None:

    numer_of_marks = find_numer_of_marks_by_students(my_students)
    group_of_student = find_group_by_students(my_students)

    list_of_marks = []
    received_marks = {}

    for id_student in range(1, NUMBER_STUDENTS + 1):
        received_marks[id_student] = 0

    number_of_students_in_group = {}
    for id_student in range(1, NUMBER_STUDENTS + 1):
        number_of_students_in_group[group_of_student[id_student]] = 0

    students_of_group = [[], [], [], []]
    for id_student in range(1, NUMBER_STUDENTS + 1):
        id_group = group_of_student[id_student]
        number_of_students_in_group[id_group] += 1
        students_of_group[id_group].append(id_student)

    for number_of_week in range(7):
        if numer_of_marks == received_marks:
            break
        for number_of_day in range(5):
            date_of_mark = START_DATE + timedelta(number_of_week * 7 + number_of_day)
            for number_of_group in range(1, NUMBER_GROUPS + 1):
                if number_of_students_in_group[number_of_group] == 0:
                    continue
                for number_of_class in range(4):
                    id_subject = randint(1, NUMBER_SUBJECTS)
                    number_of_marks_in_class = randint(
                        0, number_of_students_in_group[number_of_group]
                    )
                    id_students_by_marks_of_class = []
                    for mark in range(number_of_marks_in_class):
                        while True:
                            id_student_by_mark = students_of_group[number_of_group][
                                randint(
                                    0, number_of_students_in_group[number_of_group] - 1
                                )
                            ]
                            if id_student_by_mark not in id_students_by_marks_of_class:
                                id_students_by_marks_of_class.append(id_student_by_mark)
                                break
                        list_of_marks.append(
                            (
                                randint(*MARKS_RANGE),
                                date_of_mark,
                                id_subject,
                                id_student_by_mark,
                            )
                        )
                        received_marks[id_student_by_mark] += 1
                        if (
                            received_marks[id_student_by_mark]
                            == numer_of_marks[id_student_by_mark]
                        ):
                            number_of_students_in_group[number_of_group] -= 1
                            students_of_group[number_of_group].remove(
                                id_student_by_mark
                            )

    for mark_info in list_of_marks:
        session.add(
            Mark(
                value=mark_info[0],
                date_of=mark_info[1],
                subject_id_fn=mark_info[2],
                student_id_fn=mark_info[3],
            )
        )
    session.commit()


if __name__ == "__main__":
    engine = create_engine(DB_URL, echo=False)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    fill_table_groups()
    my_students = fill_table_students()
    fill_table_lectors()
    fill_table_subjects()
    fill_table_marks(my_students)
