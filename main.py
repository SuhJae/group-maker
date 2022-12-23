from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/groups", methods=["POST"])
def groups():
    students = request.form["students"].split("\n")
    if request.form["students_per_group"] == "":
        return render_template("failure.html")
    else:
        students_per_group = int(request.form["students_per_group"])
    distribute_leftovers = request.form.get("distribute_leftovers") == "on"

    if len(students) < 1:
        return render_template("failure.html")
    if students_per_group < 1:
        return render_template("failure.html")
    if len(students) < students_per_group:
        return render_template("failure.html")
    else:
        groups = []
        current_group = []
        for i, student in enumerate(students):
            current_group.append(student)
            if (i + 1) % students_per_group == 0:
                groups.append(current_group)
                current_group = []
        if current_group:
            if distribute_leftovers and len(groups):
                random.shuffle(current_group)
                while current_group:
                    for i in range(len(groups)):
                        if current_group:
                            groups[i].append(current_group.pop())
            else:
                groups.append(current_group)


    return render_template("groups.html", groups=groups)

if __name__ == "__main__":
    app.run()
