# .\env\Scripts\activate.ps1


from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

test_app = Flask(__name__)
test_app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///TODO.db"
db = SQLAlchemy(test_app)

class TodoData(db.Model):
    Sl = db.Column(db.Integer, primary_key = True)
    TodoName = db.Column(db.String(50), nullable = False)
    TodoDescription = db.Column(db.String(250), nullable = False)

    def __repr__(self) -> str:
        return f"{self.Sl} -> {self.TodoName} -> {self.TodoDescription}"


@test_app.route('/', methods=['GET','POST'])
def test_main():
    if request.method == 'POST':
        TodoName = request.form['TodoName']
        TodoDescription = request.form['TodoDescription']
        todoData = TodoData(TodoName = TodoName, TodoDescription = TodoDescription)
        db.session.add(todoData)
        db.session.commit()

    allTodoData = TodoData.query.all()

    return render_template('index.html', allTodoData = allTodoData)
    #return "Hello World"

@test_app.route('/delete/<int:Sl>')
def test_delete(Sl):
    TodoDelete = TodoData.query.filter_by(Sl = Sl).first()
    db.session.delete(TodoDelete)
    db.session.commit()
    return redirect('/')

@test_app.route('/update/<int:Sl>', methods=['GET','POST'])
def test_update(Sl):
    if request.method == 'POST':
        TodoName = request.form['TodoName']
        TodoDescription = request.form['TodoDescription']
        TodoUpdate = TodoData.query.filter_by(Sl = Sl).first()
        TodoUpdate.TodoName = TodoName
        TodoUpdate.TodoDescription = TodoDescription
        db.session.add(TodoUpdate)
        db.session.commit()
        return redirect('/')

    TodoUpdate = TodoData.query.filter_by(Sl = Sl).first()    
    return render_template('update.html', TodoUpdate = TodoUpdate)


if __name__ == "__main__":
    with test_app.app_context():
        db.create_all()
    test_app.run(debug=True, port=8000)
