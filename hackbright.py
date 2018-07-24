"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchone()

    print("Student: {} {}\nGitHub account: {}".format(row[0], row[1], row[2]))


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    # SQL query command format
    QUERY = """
    	INSERT INTO students (first_name, last_name, github)
    		VALUES (:fn, :ln, :gith)

    """

    # build and execute SQL query
    db.session.execute(QUERY, {'fn': first_name, 
    							'ln': last_name, 
    							'gith': github})

    # save inserted data in database
    db.session.commit()

    # report success
    print(f"Succesfully added student: {first_name} {last_name}")


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    # SQL query format
    QUERY = """ 
    		SELECT title, description, max_grade
    		FROM projects
    		WHERE title = :title
    """

    # build and execute query (get query object back)
    cursor = db.session.execute(QUERY, {'title': title})

    # give us the record as a tuple (title, description, max_grade)
    record = cursor.fetchone()

    # print things to user
    print("Title: {}\nDescription: {}\nMax Grade on Project: {}".format(record[0], 
    														record[1], record[2]))


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    
    QUERY = """ 
    		SELECT student_github, project_title
    		FROM grades
    		WHERE student_github = :github AND project_title = :title

    """
    cursor = db.session.execute(QUERY, {'github': github, 
    									'title': title})

    record = cursor.fetchone()

    #print("{} get a grade {} on the {}".format(record[0], record[2], record[1]))

def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    pass


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        else:
            if command != "quit":
                print("Invalid Entry. Try again.")


if __name__ == "__main__":
    connect_to_db(app)

    #handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
