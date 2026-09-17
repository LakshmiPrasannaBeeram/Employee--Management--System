
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)

# Secret key for flash messages
app.secret_key = "employee_management_secret_key"


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_db_connection():

    connection = sqlite3.connect("employee.db")

    # Allows us to use column names like employee["name"]
    connection.row_factory = sqlite3.Row

    return connection


# ==================================================
# CREATE DATABASE TABLES
# ==================================================

def create_tables():

    connection = get_db_connection()

    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)


    # Employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            position TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            salary REAL NOT NULL
        )
    """)


    connection.commit()

    connection.close()


# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
@app.route("/home")
def home():

    return render_template("home.html")


# ==================================================
# REGISTER
# ==================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form.get("fullname")
        username = request.form.get("username")
        password = request.form.get("password")


        connection = get_db_connection()

        cursor = connection.cursor()


        try:

            cursor.execute("""
                INSERT INTO users
                (fullname, username, password)
                VALUES (?, ?, ?)
            """, (fullname, username, password))


            connection.commit()

            flash("Successfully Registered!", "success")

            connection.close()

            return redirect(url_for("login"))


        except sqlite3.IntegrityError:

            connection.close()

            flash("Username already exists!", "error")

            return redirect(url_for("register"))


    return render_template("register.html")


# ==================================================
# LOGIN
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")


        connection = get_db_connection()

        cursor = connection.cursor()


        cursor.execute("""
            SELECT * FROM users
            WHERE username = ? AND password = ?
        """, (username, password))


        user = cursor.fetchone()

        connection.close()


        if user:

            flash("Login successful!", "success")

            return redirect(url_for("home"))


        else:

            flash("Invalid username or password!", "error")

            return redirect(url_for("login"))


    return render_template("login.html")


# ==================================================
# VIEW ALL EMPLOYEES
# ==================================================

@app.route("/employees")
def view_employees():

    connection = get_db_connection()

    employees = connection.execute("""
        SELECT * FROM employees
        ORDER BY id
    """).fetchall()

    connection.close()


    return render_template(
        "employees.html",
        employees=employees
    )


# ==================================================
# ADD EMPLOYEE
# ==================================================

@app.route("/addemployee", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        name = request.form.get("name")
        department = request.form.get("department")
        position = request.form.get("position")
        email = request.form.get("email")
        phone = request.form.get("phone")
        salary = request.form.get("salary")


        connection = get_db_connection()


        connection.execute("""
            INSERT INTO employees
            (name, department, position, email, phone, salary)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            department,
            position,
            email,
            phone,
            salary
        ))


        connection.commit()

        connection.close()


        flash("Employee added successfully!", "success")

        return redirect(url_for("view_employees"))


    return render_template(
        "addemployee.html",
        employee=None
    )


# ==================================================
# EDIT EMPLOYEE
# ==================================================

@app.route("/addemployee/<int:employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):

    connection = get_db_connection()


    # ----------------------------------------------
    # UPDATE EMPLOYEE
    # ----------------------------------------------

    if request.method == "POST":

        name = request.form.get("name")
        department = request.form.get("department")
        position = request.form.get("position")
        email = request.form.get("email")
        phone = request.form.get("phone")
        salary = request.form.get("salary")


        connection.execute("""
            UPDATE employees
            SET
                name = ?,
                department = ?,
                position = ?,
                email = ?,
                phone = ?,
                salary = ?
            WHERE id = ?
        """, (
            name,
            department,
            position,
            email,
            phone,
            salary,
            employee_id
        ))


        connection.commit()

        connection.close()


        flash("Employee details updated successfully!", "success")

        return redirect(url_for("view_employees"))


    # ----------------------------------------------
    # GET EMPLOYEE DETAILS
    # ----------------------------------------------

    employee = connection.execute("""
        SELECT * FROM employees
        WHERE id = ?
    """, (employee_id,)).fetchone()


    connection.close()


    if employee is None:

        flash("Employee not found!", "error")

        return redirect(url_for("view_employees"))


    return render_template(
        "addemployee.html",
        employee=employee
    )


# ==================================================
# DELETE EMPLOYEE
# ==================================================

@app.route("/deleteemployee/<int:employee_id>")
def delete_employee(employee_id):

    connection = get_db_connection()


    connection.execute("""
        DELETE FROM employees
        WHERE id = ?
    """, (employee_id,))


    connection.commit()

    connection.close()


    flash("Employee deleted successfully!", "success")

    return redirect(url_for("view_employees"))


# ==================================================
# SEARCH EMPLOYEE
# ==================================================

@app.route("/search")
def search():

    query = request.args.get("query", "").strip()


    connection = get_db_connection()


    # If search box is empty
    if query == "":

        employees = []


    else:

        search_value = "%" + query + "%"


        employees = connection.execute("""
            SELECT * FROM employees
            WHERE
                name LIKE ?
                OR CAST(id AS TEXT) LIKE ?
                OR department LIKE ?
                OR position LIKE ?
                OR email LIKE ?
                OR phone LIKE ?
        """, (
            search_value,
            search_value,
            search_value,
            search_value,
            search_value,
            search_value
        )).fetchall()


    connection.close()


    return render_template(
        "search.html",
        employees=employees
    )


# ==================================================
# START APPLICATION
# ==================================================

if __name__ == "__main__":

    create_tables()

    app.run(debug=True)

