
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = "employee_secret_key"


# Store registered users
users = []


# Store employee details
employees = []


# ==============================
# HOME PAGE
# ==============================

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


# ==============================
# REGISTER
# ==============================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        username = request.form["username"]
        password = request.form["password"]

        users.append({
            "fullname": fullname,
            "username": username,
            "password": password
        })

        # Registration success message
        flash("Successfully Registered!")

        # Go to login page
        return redirect(url_for("login"))

    return render_template("register.html")


# ==============================
# LOGIN
# ==============================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        for user in users:

            if user["username"] == username and user["password"] == password:

                flash("Login successful!")

                return redirect(url_for("employee_list"))

        flash("Invalid username or password!")

    return render_template("login.html")


# ==============================
# EMPLOYEE LIST
# ==============================

@app.route("/employees")
def employee_list():

    return render_template(
        "employees.html",
        employees=employees
    )


# ==============================
# ADD + EDIT EMPLOYEE
# ==============================

@app.route("/addemployee", methods=["GET", "POST"])
@app.route("/addemployee/<int:employee_id>", methods=["GET", "POST"])
def addemployee(employee_id=None):

    # --------------------------
    # EDIT EMPLOYEE
    # --------------------------

    if employee_id is not None:

        employee = None

        # Find employee
        for emp in employees:

            if emp["id"] == employee_id:

                employee = emp
                break

        # Employee not found
        if employee is None:

            flash("Employee not found!")

            return redirect(url_for("employee_list"))

        # Update employee
        if request.method == "POST":

            employee["name"] = request.form["name"]
            employee["email"] = request.form["email"]
            employee["phone"] = request.form["phone"]
            employee["department"] = request.form["department"]
            employee["salary"] = request.form["salary"]

            flash("Employee updated successfully!")

            return redirect(url_for("employee_list"))

        return render_template(
            "addemployee.html",
            employee=employee,
            edit_mode=True
        )


    # --------------------------
    # ADD NEW EMPLOYEE
    # --------------------------

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        salary = request.form["salary"]

        new_employee = {

            "id": len(employees) + 1,

            "name": name,

            "email": email,

            "phone": phone,

            "department": department,

            "salary": salary
        }

        employees.append(new_employee)

        flash("Employee added successfully!")

        return redirect(url_for("employee_list"))


    return render_template(
        "addemployee.html",
        employee=None,
        edit_mode=False
    )


# ==============================
# DELETE EMPLOYEE
# ==============================

@app.route("/deleteemployee/<int:employee_id>")
def deleteemployee(employee_id):

    for employee in employees:

        if employee["id"] == employee_id:

            employees.remove(employee)

            flash("Employee deleted successfully!")

            break

    return redirect(url_for("employee_list"))


# ==============================
# SEARCH EMPLOYEE
# ==============================

@app.route("/search", methods=["GET", "POST"])
def search():

    results = []

    if request.method == "POST":

        search_name = request.form["search_name"].lower()

        for employee in employees:

            if search_name in employee["name"].lower():

                results.append(employee)

    return render_template(
        "search.html",
        results=results
    )


# ==============================
# START SERVER
# ==============================

if __name__ == "__main__":

    app.run(debug=True)


