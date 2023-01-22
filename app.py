from apiflask import APIFlask, abort
from flask import jsonify
from db import session, Task
from schemas import TaskOutputSchema, TaskCreationSchema, TaskUpdateSchema


app = APIFlask(__name__)

@app.get('/')
def index():
    return {"message": "Hello World"}

'''
    get /task get_all_task
    post /tasks create task
    get /task/<task_id> get_task_by_id
    put /task/<task_id> update_task
    delete /<task_id> delete_task

'''

@app.get('/')
def get_all_tasks():
    posts = session.query(Task).all()

    schema = TaskOutputSchema()
    result = schema.dump(posts, many=True)

    return jsonify(result)

@app.post('/tasks')
@app.input(TaskCreationSchema)
@app.output(TaskOutputSchema)
def create_task(data):
    content = data.get('content')

    new_task = Task(content=content)

    session.add(new_task)
    session.commit()

    return new_task, 201


@app.get('/tasks/<int:task_id>')
@app.output(TaskOutputSchema) 
def get_task_by_id(task_id):
    task = session.query(Task).filter_by(id=task_id).first()

    if task is not None:
        return task, 200

    abort(404)

@app.put('/tasks/<int:task_id>')
@app.input(TaskUpdateSchema)
@app.output(TaskOutputSchema)
def update_task(task_id, data):
    content = data.get('content')
    is_completed = data.get('is_completd')

    task_to_update = session.query(Task).filter_by(id=task_id).first()
    task_to_update.content = content
    task_to_update.is_completed = is_completed

    session.commit()
    return task_to_update

@app.delete('/tasks/<int:task_id>')
def delete_task (task_id):
    task_to_delete= session.query(Task).filter_by(id=task_id).first()

    session.delete(task_to_delete)
    session.commit()
    return{"Message":"Deleted"}, 204