from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content =db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.content}>'

class TodoSchema(ma.Schema):
    class Meta:
        ordered = True
        fields = ('id','content','date_added')
        


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)


@app.route('/', methods = ['POST' ,'GET'])
def add_task():
    if request.method=='POST':

        content = request.json['content']
        new_task = Todo(content=content)
        db.session.add(new_task)
        db.session.commit()
        return todo_schema.jsonify(new_task)
    else:
        tasks = Todo.query.all()
        return todos_schema.jsonify(tasks)



if __name__ == '__main__':
    app.run(debug=True)








