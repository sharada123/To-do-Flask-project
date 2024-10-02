'''
module name - flask
class name - Flask
'''
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#create object of flask class
app=Flask('__name__')
# Configure the MySQL database URI 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"{self.id} - { self.title}"


@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    context={}
    context['alltodo']=alltodo
    return render_template('index.html',**context)

@app.route('/delete/<int:id>')
def delete(id):
    todo=Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.get(id)
        todo.title=title
        todo.desc=desc
        todo.date_created=datetime.now()
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.get(id)
    context={}
    context['todo']=todo
    return render_template('update.html',**context)
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()         #to create database and table in database
    app.run(debug=True)         #run the server, there is method named run() inside Flask class

