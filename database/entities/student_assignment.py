from database.database_connection import *
from database.entities.student import Student
from database.entities.assignment import Assignment


class StudentAssignment:
    student = ForeignKeyField(Student)
    assignment = ForeignKeyField(Assignment)

    class Meta:
        database = db
