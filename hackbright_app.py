import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def make_new_project(project_title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) values (?, ?, ?)"""
    DB.execute(query, (project_title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s %s %s" % (project_title, description, max_grade)


def find_projects_by_title(project_title):
    query = """SELECT title, description FROM Projects WHERE title = ?"""
    DB.execute(query, (project_title, ))
    row = DB.fetchone()
    print '%s, %s' % (row[0], row[1])

def get_grade_by_student(project_title, github):
    query = """SELECT Students.first_name, Students.last_name, Grades.grade 
               FROM Grades JOIN Students ON (Grades.student_github = Students.github) 
               WHERE project_title = ? AND github = ?"""
    DB.execute(query, (project_title, github))
    row = DB.fetchone()
    print 'Student %s %s got a grade of %s' % (row[0], row[1], row[2])

def show_all_grades(first_name, last_name):
    query = """SELECT Students.first_name, Students.last_name, Grades.grade 
               FROM Grades JOIN Students ON (Grades.student_github = Students.github) 
               WHERE Students.first_name = ? AND Students.last_name = ?"""
    DB.execute(query, (first_name, last_name))
    data = DB.fetchall()
    print "Student: %s %s" % (data[0][0], data[0][1])
    for item in data:
        print item[2]

def give_grade_student(github, project_title, grade):
    query = """INSERT into Grades values (?, ?, ?)"""
    DB.execute(query, (github, project_title, grade))
    CONN.commit()
    print "Gave student %s grade: %s for project: %s" %(github, project_title, grade)

def main():
    connect_to_db()

    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
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

    CONN.close()

if __name__ == "__main__":
    main()

# to do :
# add ability for spaces
# check for errors
# help text
