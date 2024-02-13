from flask import Flask,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta

app = Flask(__name__)
app.secret_key='hdfdfkjgfjgfjlfgdj'
app.config['SESSION_COOKIE_NAME'] = 'custom_session_cookie'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    status = db.Column(db.Boolean,nullable=True)

# Set up application context
app_context = app.app_context()
app_context.push()

with app.app_context():
    db.create_all()
app_context.pop()


@app.route('/',methods=['POST','GET'])
def home():
    # Create Task and add to Database
    if request.method == 'POST':
        task_name = request.form.get('task')
        task_status = request.form.get('status',False)
        task = Task(title=task_name,status=task_status)
        db.session.add(task)
        db.session.commit()

    # Get all Tasks from Database
    tasks = db.session.query(Task).all()     

    return render_template('tasks.html',tasks=tasks)


if __name__=='__main__':
   app.run(debug=True)