from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)

db_user = 'root'
db_pass = '12345678'
db_name = 'tasklist'
db_host = 'localhost'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Tasklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tasklist


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Tasklist.query.all()
    return jsonify(tasks_schema.dump(tasks))


@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json.get('description', '')
    task = Tasklist(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    return jsonify(task_schema.dump(task))


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = db.session.get(Tasklist, id)
    return jsonify(task_schema.dump(task))


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = db.session.get(Tasklist, id)
    title = request.json['title']
    description = request.json.get('description', '')
    task.title = task.title if not title else title
    task.description = task.description if not description else description
    task.updated_at = datetime.now()
    db.session.commit()
    return jsonify(task_schema.dump(task))


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = db.session.get(Tasklist, id)
    db.session.delete(task)
    db.session.commit()
    return 'Успешно удалено', 204


if __name__ == '__main__':
    app.run(debug=True)