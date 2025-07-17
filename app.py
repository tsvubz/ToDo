# Imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# My App setup
app = Flask(__name__)
Scss(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tbase.db'
db = SQLAlchemy(app)

# Models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"

# Routes to Web Pages
@app.route('/', methods=['GET', 'POST'])
def index():
    # Add Task
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = Task(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error adding task: {e}")
            return f"Error adding task: {e}"
    # See current Tasks
    else:
        tasks = Task.query.order_by(Task.created_at).all()
        return render_template('index.html', tasks=tasks)







# Runner and Debugger
if __name__ == '__main__':
    with app.app_context():
        db.create_all()


    app.run(debug=True)
