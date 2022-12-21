from flask import Flask, redirect, url_for, render_template, request
from todo_app.data.session_items import get_items,get_item,add_item,save_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/index')
def index():
    items=get_items()
    return render_template('index.html', items=items)

@app.route('/add_todo_item', methods=['POST'])
def add_todo_item():
    new_item_title = request.form.get('title')
    add_item(new_item_title)
    print("add_todo_item")
    return redirect(url_for('index'))

@app.route('/item_completed', methods=['POST'])
def item_completed():
    completed_item_id = request.form.get('id')
    save_item(get_item(completed_item_id))
    print("item_completed")
    return redirect(url_for('index'))
