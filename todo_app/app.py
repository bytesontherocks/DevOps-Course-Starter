from flask import Flask, redirect, url_for, render_template, request
from todo_app.data.session_items import get_items,add_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/index')
def index():
    items=get_items()
    
    return render_template('index.html', items=items)

@app.route('/index', methods=['POST'])
def add_todo_item():
    new_item_id = request.form.get('title')
    add_item(new_item_id)
    return redirect(url_for('index'))
