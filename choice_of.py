from sqlalchemy import create_engine, select

from sqlalchemy.orm import sessionmaker

from models import Group, Student, Lector, Subject

from models import DB_URL

from auxiliary_functions import input_in_range


def choice_of(my_class) -> tuple[int, str]:
    engine = create_engine(DB_URL, echo=False)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    stmt = select(my_class.id, my_class.name).order_by(my_class.id)
    list_of_choice = session.execute(stmt).all()

    [print(f"{choice[0]} - {choice[1]}") for choice in list_of_choice]
    choice_number = input_in_range("Enter the subject number", 1, len(list_of_choice))

    return list_of_choice[choice_number - 1]


def choice_of_subject() -> tuple[int, str]:
    return choice_of(Subject)


def choice_of_lector() -> tuple[int, str]:
    return choice_of(Lector)


def choice_of_group() -> tuple[int, str]:
    return choice_of(Group)


def choice_of_student() -> tuple[int, str]:
    return choice_of(Student)
