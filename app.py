# Imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# My App
app = Flask(__name__)
Scss(app)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

# Data class - Row of data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        # This provides a string representation of an object
        return f"Task {self.id}"

with app.app_context():
    db.create_all()

# Routes to webpages
# Home page
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # Add a Task
        current_task = request.form['content']
        new_task = MyTask(content=current_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"    
    else:
        # See all current Tasks
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)

# Delete a task
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"

# Edit a task
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR:{e}"
    else:
        return render_template('edit.html', task=task)


# Runner and debugger
if __name__ == "__main__":
    app.run(debug=True)