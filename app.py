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
# db.create_all()


##Cafe TABLE Configuration
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)



@app.route('/',methods=['POST','GET'])
def home():


    # Create Task and to Database
    if request.method == 'POST':
        task_name = request.form.get('task')
        task = Task(name=task_name)
        db.session.add(task)
        db.session.commit()

    # Get all Tasks from Database
    tasks = db.session.query(Task).all()    


    return render_template('tasks.html',tasks=tasks)


if __name__=='__main__':
   app.run(debug=True)