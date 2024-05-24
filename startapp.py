############################################################################
"""
RESTful API для управления списком задач
"""
############################################################################

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)

"""
Блок настроек для работы с базой данных.
db_user - пользователь, зарегистрированный в MySQL;
db_pass - пароль;
db_name - наименование базы данных;
db_host - адрес хоста, где запущена MySQL;
db_port - адрес порта, через который проходит подключение. Необязательный.
"""
db_user = 'root'
db_pass = '12345678'
db_name = 'tasklist'
db_host = 'localhost'
db_port = ':3306'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql://{db_user}:{db_pass}@{db_host}{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Tasklist(db.Model):
    """
    Модель списка задач.
    Содержит поля:
    id - идентификатор задачи, уникальный номер;
    title - наименование задачи;
    description - полное описание задачи;
    created_at - дата и время создания задачи;
    updated_at - дата и время обновления задачи.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class TaskSchema(ma.SQLAlchemyAutoSchema):
    """
    Схема для работы с данными.
    """
    class Meta:
        model = Tasklist


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Получить полный список всех задач.
    На выходе: JSON-список задач, где каждая задача представляет собой
    JSON-объект с полями id, title, description, created_at, updated_at.
    """
    tasks = Tasklist.query.all()
    return jsonify(tasks_schema.dump(tasks))


@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Создать задачу.
    На входе: JSON-объект с полями title (строка) и
    description (строка, опционально).
    На выходе: JSON-объект с полями id, title, description, created_at,
    updated_at.
    """
    title = request.json['title']
    description = request.json.get('description', '')
    task = Tasklist(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    return jsonify(task_schema.dump(task))


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    """
    Получить данные по задаче.
    На выходе: JSON-объект с полями id, title, description, created_at,
    updated_at.
    """
    task = db.session.get(Tasklist, id)
    return jsonify(task_schema.dump(task))


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    """
    Создать задачу.
    На входе: JSON-объект с полями title (строка, опционально) и
    description (строка, опционально).
    На выходе: JSON-объект с полями id, title, description, created_at,
    updated_at.
    Поставлена проверка на опциональные параметры. Если пустое значение,
    данные не изменяются.
    """
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
    """
    Удалить задачу.
    На выходе: Сообщение об успешном удалении.
    """
    task = db.session.get(Tasklist, id)
    if task is None:
        return {
            'id': id,
            'сообщение': 'Задача отсутствует'
        }, 404
    title = task.title
    db.session.delete(task)
    db.session.commit()
    return {
        'id': id,
        'сообщение': f'Задача "{title}" успешно удалена'
    }, 204


# Основной запуск
if __name__ == '__main__':
    app.run(debug=True)

############################################################################
