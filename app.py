from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/',methods=['POST','GET'])
def home():
    tasks=[]
    task = request.form.get('task')
    tasks.append(task)
    return render_template('tasks.html',tasks=tasks)


if __name__=='__main__':
   app.run(debug=True)