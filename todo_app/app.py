from flask import Flask, redirect, url_for, render_template, request
from todo_app.data.trello_items import get_items,add_item,move_card_to_new_list
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    items=get_items()    
    return render_template('index.html', items=items)

@app.route('/', methods=['POST'])
def add_todo_item():
    new_item_title = request.form.get('title')
    add_item(new_item_title)
    return redirect(url_for('index'))

@app.route('/complete_item<id>')
def mark_item_as_complete(id):
    move_card_to_new_list(int(id), 'To Do', 'Done')
    return redirect(url_for('index'))

@app.route('/todo<id>')
def mark_item_as_todo(id):
    move_card_to_new_list(int(id), 'Done', 'To Do')
    return redirect(url_for('index'))