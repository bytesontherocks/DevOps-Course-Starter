import os
import pytest
from threading import Thread
from time import sleep
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from dotenv import load_dotenv
from todo_app import app
import requests

headers = {
  "Accept": "application/json"
}

query = {
  'key': os.getenv('TRELLO_API_KEY'),
  'token': os.getenv('TRELLO_API_TOKEN')
}

testing_board = {
    'name' : 'e2e_testing_board',
    'id' : '-1'
}

@pytest.fixture(scope='module')
def app_with_temp_board():
    # Load our real environment variables
    load_dotenv(override=True)

    # Create the new board & update the board id environment variable
    board_id = create_trello_board()
    os.environ['TRELLO_BOARD_ID'] = board_id

    # Construct the new application
    application = app.create_app()

    # Start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    
    # Give the app a moment to start
    sleep(1)

    # Return the application object as the result of the fixture
    yield application

    # Tear down
    thread.join(1)
    delete_trello_board(board_id)

def create_trello_board():
    url = "https://api.trello.com/1/boards/"

    query['name'] = testing_board['name']

    response = requests.post(
        url,
        headers=headers,
        params=query
    )

    if response.status_code == 200:
        resp_json = response.json()
        testing_board['id'] = resp_json['id']
        #print(f"Print new testing board id: {testing_board['id']}")
    
    return testing_board['id']

def delete_trello_board(board_id):
    url = "https://api.trello.com/1/boards/{board_id}"

    response = requests.delete(
        url,
        headers=headers,
        params=query
    )
    
    pass

@pytest.fixture(scope="module")
def driver():
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    with webdriver.Firefox(options=opts) as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'