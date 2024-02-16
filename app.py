from flask import Flask,render_template,request,session,jsonify,redirect,url_for
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


@app.route('/',methods=['GET','POST'])
def home():
    # Get all Tasks from Database
    tasks = db.session.query(Task).all()     
    return render_template('tasks.html',tasks=tasks)

@app.route('/add',methods=['POST'])
def add_task():
        # Create Task and add to Database
    if request.method == 'POST':
        task_name = request.form.get('task')
        task_status = request.form.get('status',False)
        task = Task(title=task_name,status=task_status)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('home'))
    
    # return render_template('tasks.html')



@app.route('/active')
def task_active():
    active_tasks = db.session.query(Task).filter_by(status=False)
    return render_template('tasks.html',tasks=active_tasks)

@app.route('/completed')
def task_complete():
    completed_tasks = db.session.query(Task).filter_by(status=True)
    return render_template('tasks.html',tasks=completed_tasks)



# Route to display tasks and update them
@app.route('/tasks', methods=['GET', 'POST'])
def task_list(task_id):
    if request.method == 'POST':
        tasks= db.session.query(Task).all()

        for task in tasks:
            if task.id == task_id:
                print(f"------{task_id}......")
                task.status = True  # Update task as completed
                db.session.commit()
                break
        return redirect(url_for('task_complete'))

    return render_template('tasks.html', tasks=tasks)


# # Route to update task status
# @app.route('/tasks/update', methods=['POST'])
# def update_task():
#     task_id = request.form.get('id')
#     tasks= db.session.query(Task).all()
#     for task in tasks:
#         if task.id == task_id:
#             print(task.id)
#             task.status = True # Toggle task completion status
#             break
#     return redirect( url_for('task_complete'))


if __name__=='__main__':
   app.run(debug=True)