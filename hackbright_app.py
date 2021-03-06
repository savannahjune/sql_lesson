import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    if row:
        return row
    else:
        return "Student does not exist."

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    return [first_name, last_name, github]

def make_new_project(project_title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) values (?, ?, ?)"""
    DB.execute(query, (project_title, description, max_grade))
    CONN.commit()
    return "Successfully added project: %s, %s, %s" % (project_title, description, max_grade)


def find_projects_by_title(project_title):
    query = """SELECT title, description FROM Projects WHERE title = ?"""
    DB.execute(query, (project_title, ))
    row = DB.fetchone()
    if row:
        return "%s, %s" % (row[0], row[1])
    else:
        return "Project does not exist."

def get_grades_by_project(project_title):
    query="""SELECT * FROM Grades WHERE project_title = ?"""
    DB.execute(query, (project_title, ))
    data = DB.fetchall()
    if data:
        return data
    else: 
        return "Project does not exist."

def get_grade_by_student(project_title, github):
    query = """SELECT Students.first_name, Students.last_name, Grades.grade 
               FROM Grades JOIN Students ON (Grades.student_github = Students.github) 
               WHERE project_title = ? AND github = ?"""
    DB.execute(query, (project_title, github))
    row = DB.fetchone()
    if row:
        return "Student %s %s got a grade of %s" % (row[0], row[1], row[2])
    else:
        return "Project or student does not exist."

def show_all_grades(github):
    query = """SELECT Students.first_name, Students.last_name, Grades.project_title, Grades.grade 
               FROM Grades JOIN Students ON (Grades.student_github = Students.github) 
               WHERE Students.github = ?"""
    DB.execute(query, (github,))
    data = DB.fetchall()
    if data:
        return data

    else:
        return "Student does not exist."

def give_grade_student(github, project_title, grade):
    query = """INSERT into Grades values (?, ?, ?)"""
    DB.execute(query, (github, project_title, grade))
    CONN.commit()
    return "Gave student %s grade: %s for project: %s" %(github, project_title, grade)


def main():
    connect_to_db()

    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(',')
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args)
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project_title":
            find_projects_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "grade":
            get_grade_by_student(*args)
        elif command == "give_grade":
            give_grade_student(*args)
        elif command == "show_all_grades":
            show_all_grades(*args)
        elif 'help' in command:
            return """Be sure to comma separate all of your inputs with NO SPACES!\n
Find student: Enter 'student' followed by the student's github username.\n
Add student: Enter 'new_student' followed by the student's first name, last name, and github.\n
Find project description: Enter 'project_title' followed by the project's title\n
Add project: Enter 'new_project' followed by the project title, description and max grade\n
Find student grade: Enter 'grade' followed by the project title and student's github.\n
Give student grade: Enter 'give_grade' followed by the student's github, project title, and grade.\n
Show all grades for student: Enter 'show_all_grades' followed by the student's first and last name."""
        else:
            return "I'm sorry. I don't understand that command. Type 'help' for more information!"

    CONN.close()

if __name__ == "__main__":
    main()
