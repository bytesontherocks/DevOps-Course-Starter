import os
import pytest
from dotenv import find_dotenv, load_dotenv
from todo_app import app
import requests


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    # This replaces any call to requests.get with our own function
    monkeypatch.setattr(requests, 'get', stub)

    response = client.get('/')

    decoded_data = response.data.decode()

    assert response.status_code == 200
    assert 'Test card to do' in decoded_data
    assert 'Test card done' in decoded_data
class StubResponse():
    def __init__(self, fake_response_data, fake_status_code):
        self.fake_response_data = fake_response_data
        self.status_code = fake_status_code
    def json(self):
        return self.fake_response_data


def stub(url, headers={}, params={}):
    test_board_id = os.environ.get('TRELLO_BOARD_ID')
    fake_response_data = None
    
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [
            {
                'id': '123abc',            
                'name': 'To Do',
                'cards': [{'id': '456', 'idShort': '34','name': 'Test card to do'}]
            },
            {
                'id': '787878',            
                'name': 'Done',
                'cards': [{'id': '2984', 'idShort': '28','name': 'Test card done'}]
            }
        ]
        return StubResponse(fake_response_data, 200)
    
    raise Exception(f'Integration test did not expect URL "{url}"')