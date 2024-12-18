from flask import Flask , render_template, request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime  import datetime
app = Flask(__name__)   # Flask constructor 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class Todo(db.Model):
    sno= db.Column(db.Integer,primary_key=True)
    title =db.Column(db.String(200),nullable=False)
    desc =db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"

   
# A decorator used to tell the application 
# which URL is associated function 
@app.route('/' , methods =['GET' , 'POST'])       
def hello():
    if request.method=="POST":
        title =request.form['title']
        desc =request.form['desc']
        todo =Todo(title=title ,desc =desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template('index.html' , allTodo=allTodo)
@app.route('/show')
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return 'this is my products' 

@app.route('/update/<int:sno>' , methods =['GET' , 'POST'])
def update(sno):

    if request.method=="POST":
        title =request.form['title']
        desc =request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title 
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html' , todo=todo)


@app.route('/delete/<int:sno>')
def Delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.cli.command("create-db")
def create_db():
    """Create the database tables."""
    db.create_all()
    print("Database tables created!")
if __name__=='__main__':  
   
   
   app.run(debug=True) 

