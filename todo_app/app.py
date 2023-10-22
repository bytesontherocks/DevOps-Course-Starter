from todo_app.data.ViewModel import ViewModel
from flask import Flask, redirect, render_template, request, url_for

from todo_app.data.db_items import (add_item, get_items,
                                        move_card_to_new_list)
from todo_app.flask_config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    @app.route('/')
    def index():
        items=get_items()    
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/', methods=['POST'])
    def add_todo_item():
        new_item_title = request.form.get('title')
        add_item(new_item_title)
        return redirect(url_for('index'))

    @app.route('/complete_item/<id>', methods=['POST'])
    def mark_item_as_complete(id):
        move_card_to_new_list(int(id), 'To Do', 'Done')
        return redirect(url_for('index'))

    @app.route('/todo/<id>', methods=['POST'])
    def mark_item_as_todo(id):
        move_card_to_new_list(int(id), 'Done', 'To Do')
        return redirect(url_for('index'))
    
    return app
