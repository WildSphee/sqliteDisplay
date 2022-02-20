import sqlite3 as db
from sqlite3 import Error
import tkinter as tk
import random

database = "customers.db"
random_names = ['mia', 'jorge', 'john', 'fernado', 'brian', 'kenny', 'minting', 'robin', 'larry', 'jerry', 'kelly', 'herman',
                'emily', 'kelvin', 'juan', 'calvin', 'ashley', 'yanny', 'reagan']




def createConnection(cdatabase):

    conn = None
    try:
        conn = db.connect(cdatabase)
    except Error:
        print(Error)
    return conn

def create_random_students(conn, numOfStudents = 1, ranlist = random_names):
    sql = '''
        INSERT INTO Students (name, id, age) VALUES (?,?,?);
        '''
    c = conn.cursor()
    # lastrow = c.execute("SELECT * FROM Students;").lastrowid
    # print(lastrow)
    selectedlis = random.sample(ranlist, numOfStudents)
    for i in range(len(selectedlis)):
        c.execute(sql, (selectedlis[i].capitalize(), i+1, random.randint(18, 30)))

    conn.commit()

def create_course(conn, course):
    sql = '''
    INSERT INTO Courses (name) VALUES (?);
    '''
    c = conn.cursor()
    c.execute(sql, course)
    conn.commit()
    return c.lastrowid

def create_student(conn, student):
    sql = '''
    INSERT INTO Students (name, id, age) VALUES (?,?,?);
    '''
    c = conn.cursor()
    c.execute(sql, student)
    conn.commit()
    return c.lastrowid

def create_student2course(conn, student_course):
    sql = '''
    INSERT INTO Student_courses (id_student, id_course) VALUES (?,?);
    '''
    c = conn.cursor()
    c.execute(sql, student_course)
    conn.commit()

def delete_student(conn, id):
    sql = '''
    DELETE FROM Student_courses WHERE id_student=?;
    '''
    c = conn.cursor()
    c.execute(sql, (id,))
    conn.commit()

    sql = '''
        DELETE FROM Students WHERE id=?;
        '''
    c = conn.cursor()
    c.execute(sql, (id,))
    conn.commit()

def delete_all_student(conn):
    sql = '''
        DELETE FROM Students;
        '''
    c = conn.cursor()
    c.execute(sql)
    conn.commit()

def delete_course(conn, id):
    sql = '''
    DELETE FROM Student_courses WHERE id_course=?;
    '''
    c = conn.cursor()
    c.execute(sql, (id,))
    conn.commit()

    sql = '''
        DELETE FROM Courses WHERE id=?;
        '''
    c = conn.cursor()
    c.execute(sql, (id,))
    conn.commit()

def getAllStudent(conn):
    c = conn.cursor()
    c.execute("""
    SELECT * FROM Students ORDER BY id ASC
    """)
    fetch = c.fetchall()
    return fetch

def updateStudent(conn, name, age, id):
    data = None
    sql = None

    if len(name) != 0 and len(age) != 0:
        data = (name, age, id)
        sql = '''
        UPDATE Students SET name= ?, age= ?, WHERE id= ?
        '''
    elif len(name) == 0:
        data = (age, id)
        sql = '''
        UPDATE Students SET age= ?, WHERE id= ?
        '''
    elif len(age) == 0:
        data = (name, id)
        sql = '''
        UPDATE Students SET name= ?, WHERE id= ?
        '''

    c = conn.cursor()
    c.execute(sql, data)
    conn.commit()

def tkdisplayData(data):

    root = tk.Tk()
    root.geometry("250x300")
    root.title("Student List")

    label1 = tk.Label(text='Student Name', font='Helvetica 10 bold').grid(row=0, column=0, padx=5, pady=2)
    label2 = tk.Label(text='ID', font='Helvetica 10 bold').grid(row=0, column=1, padx=5)
    label3 = tk.Label(text='Age', font='Helvetica 10 bold').grid(row=0, column=2)

    baserow = 2
    for r, re in enumerate(data):
        for c, ce in enumerate(re):
            label = tk.Label(text=str(ce))
            label.grid(row=r + baserow, column=c, sticky="NW", padx=10)

    root.mainloop()

def main():
    conn = createConnection(database)
        # student = ('Brian', 1, 24)
        # student_id = create_student(conn, student)
        # print(student_id)
    #
    delete_all_student(conn)
    create_random_students(conn, numOfStudents=10)
    print(getAllStudent(conn))
    tkdisplayData(getAllStudent(conn))


main()