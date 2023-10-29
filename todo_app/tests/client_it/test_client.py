import os
import pytest
from dotenv import find_dotenv, load_dotenv
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

    response = client.get('/')
    
    print(f"response {response}")
    
    decoded_data = response.data.decode()

    assert response.status_code == 200
    assert 'Test card to do' in decoded_data
    assert 'Test card done' in decoded_data

def insert_data_to_db():
    collection = mongomock.MongoClient().db.collection

    card_0 = {
       'id': '123abc',            
       'name': 'To Do',
        'cards': [{'id': '456', 'idShort': '34','name': 'Test card to do'}]
    }

    card_1 = {
                'id': '787878',            
                'name': 'Done',
                'cards': [{'id': '2984', 'idShort': '28','name': 'Test card done'}]
            }

    post_id = collection.insert_one(card_0).inserted_id
    post_id = collection.insert_one(card_1).inserted_id

    return None
    