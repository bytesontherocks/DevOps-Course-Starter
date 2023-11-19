import os
import pytest
from dotenv import find_dotenv, load_dotenv
from todo_app.data.db_items import (add_item, get_items,
                                        move_card_to_new_list)
from todo_app import app
import mongomock

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        # Create the new app.
        test_app = app.create_app()
        # Use the app to create a test_client that can be used in our tests.
        with test_app.test_client() as client:
            yield client

def test_index_page(monkeypatch, client):
 
    insert_data_to_db()

    items = get_items()

    print(f"response {items}")
    print(f"name 0 {items[0].name}")

    assert 'Test card to do' == items[0].name
    assert 'To Do' == items[0].status
    assert 'Test card done' == items[1].name
    assert 'Done' == items[1].status

def insert_data_to_db():
    collection = mongomock.MongoClient().db.collection

    add_item('Test card to do')
    done_id = add_item('Test card done')
    move_card_to_new_list(done_id, 'Done')

    return None
    