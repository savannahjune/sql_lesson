from flask import Flask, render_template, request, flash
import hackbright_app 

app = Flask(__name__)

@app.route("/student/")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    row = hackbright_app.get_student_by_github(student_github)
    data = hackbright_app.show_all_grades(student_github)
    html = render_template("student_info.html", first_name=row[0],
                                                last_name=row[1],
                                                github=row[2],
                                                project_grades=data)
    return html

@app.route("/project_grades/<project_title>")
def get_project_grades(project_title):
    hackbright_app.connect_to_db()
    data = hackbright_app.get_grades_by_project(project_title)
    html = render_template("project_grades.html", project_grades=data)
    return html

@app.route("/student_added")
def add_student():
    hackbright_app.connect_to_db()
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")
    student_info = hackbright_app.make_new_student(first_name, last_name, github)
    html = render_template("student_added.html", first_name=student_info[0],
                                                 last_name=student_info[1], 
                                                 github=student_info[2])
    return html

@app.route("/")
def load_index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug = True)