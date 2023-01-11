from flask import Flask, redirect, url_for, render_template, request
from todo_app.data.session_items import get_items,add_item,remove_item, change_status
from todo_app.flask_config import Config

app=Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items=get_items()
    return render_template('index.html', items=items)

@app.route('/add_todo_item', methods=['POST'])
def add_todo_item():
    new_item_title=request.form.get('title')
    add_item(new_item_title)
    return redirect(url_for('index'))

@app.route('/remove_todo_item', methods=['POST'])
def remove_todo_item():
    to_remove_item_id=request.form.get('id')
    remove_item(to_remove_item_id)
    return redirect(url_for('index'))

@app.route('/change_item_status', methods=['POST'])
def change_item_status():
    item_id=request.form.get('id')
    item_status=request.form.get('status')
    change_status(item_id, item_status)
    return redirect(url_for('index'))
