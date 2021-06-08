import os
import sqlite3
import pandas as pd
from time import sleep

def create_tables():
    connection = sqlite3.connect("student.bd")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Teacher (
        teacher_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Course (
        course_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Class (
        class_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        number INTEGER NOT NULL,
        year date NOT NULL,
        teacher_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id),
        FOREIGN KEY (course_id) REFERENCES Course(course_id)) """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS Lesson (
        lesson_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        lesson_date datetime NOT NULL,
        homework TEXT,
        hrs INTEGER,
        class_id INTEGER,
        FOREIGN KEY (class_id) REFERENCES Class(class_id))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Student (
        student_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        birthdate date)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Teacher_Class (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        class_id INTEGER ,
        FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id),
        FOREIGN KEY (class_id) REFERENCES Class(class_id))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Student_Class (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        application_date date,
        student_id INTEGER,
        class_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES Student(student_id),
        FOREIGN KEY (class_id) REFERENCES Class(class_id))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Student_Lesson (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        done_homework INTEGER,
        student_id INTEGER ,
        lesson_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES Student(student_id),
        FOREIGN KEY (lesson_id) REFERENCES Lesson(lesson_id))""")
    connection.commit()
    connection.close()

# Select
def select(query):
    print(query)
    connection = sqlite3.connect("student.bd")
    cursor = connection.cursor()
    data = cursor.execute(query).fetchall()
    result = {}
    for i, key in enumerate(cursor.description):
        if key[0] != None:
            key = key[0]
            result[key] = []
            if data == []:
                break
            for row in data[i]:
                result[key].append(row)

    connection.commit()
    connection.close()
    return result


def insert(query, args):
    try:
        connection = sqlite3.connect("student.bd")
        cursor = connection.cursor()
        cursor.execute(query.format(*args))
        connection.commit()
        connection.close()
        return True
    except Exception:
        print(Exception)
        return False


# queries
teacher_names = '''select name from teacher'''
group_names = '''select Course.course_name || " " || Class.number as group_name
from Course inner join Class
on Course.course_id = Class.course_id ''' 
lesson_data = '''select lesson_date as "Дата", hrs as "Кол-во_часов", count(student.student_id) as "Кол-во_учащихся"
from Teacher inner join Class on Teacher.teacher_id = Class.teacher_id
inner join Course on Course.course_id = Class.course_id
inner join Lesson on Lesson.class_id = Class.class_id
inner join Student_Lesson on Student_Lesson.lesson_id = Lesson.lesson_id
inner join Student on Student.student_id = Student_Lesson.student_id
where Teacher.name = "{0}" and Course.course_name = "{1}"
group by Lesson.lesson_id'''
create_tables()
