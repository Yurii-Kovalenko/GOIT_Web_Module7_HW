from datetime import datetime

from sqlalchemy import create_engine, Integer, String, DateTime, ForeignKey

from sqlalchemy.orm import (
    sessionmaker,
    Mapped,
    mapped_column,
    relationship,
)

from auxiliary_functions import Base

DB_URL = "sqlite:///./db/study.db"


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False)


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    group_id_fn: Mapped[int] = mapped_column(
        "group_id_fn", Integer, ForeignKey("groups.id")
    )
    group: Mapped["Group"] = relationship(Group)


class Lector(Base):
    __tablename__ = "lectors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    lector_id_fn: Mapped[int] = mapped_column(
        "lector_id_fn", Integer, ForeignKey("lectors.id")
    )
    lector: Mapped["Lector"] = relationship(Lector)


class Mark(Base):
    __tablename__ = "marks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[int] = mapped_column(Integer)
    date_of: Mapped[datetime] = mapped_column(DateTime)
    subject_id_fn: Mapped[int] = mapped_column(
        "subject_id_fn", Integer, ForeignKey("subjects.id")
    )
    subject: Mapped["Subject"] = relationship(Subject)
    student_id_fn: Mapped[int] = mapped_column(
        "student_id_fn", Integer, ForeignKey("students.id")
    )
    student: Mapped["Student"] = relationship(Student)


if __name__ == "__main__":
    engine = create_engine(DB_URL, echo=False)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.create_all(engine)
