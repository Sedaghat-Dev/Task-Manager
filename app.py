from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)

Todos_db = client.flask_database
todos = Todos_db.todos

dbdeleted = client.dbdeleted
deletedtodos = dbdeleted.deletedtodos

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'todoId' in request.form:
            # Handle editing
            todo_id = request.form['todoId']
            content = request.form['content']
            degree = request.form['degree']
            todos.update_one({"_id": ObjectId(todo_id)}, {"$set": {'content': content, 'degree': degree}})
        else:
            # Handle adding a new todo
            content = request.form['content']
            degree = request.form['degree']
            todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('index'))
    
    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)

@app.post("/<id>/delete/")
def delete(id):
    new =todos.find_one({"_id": ObjectId(id)})
    deletedtodos.insert_one({"content":new['content'], "degree":new['degree']})
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

@app.route('/deleted')
def deleted():
    all_deleted_todos = deletedtodos.find()
    return render_template('deleted_todos.html', deletedtodos = all_deleted_todos)

if __name__ == '__main__':
    app.run(debug=True)
