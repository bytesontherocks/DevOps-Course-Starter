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

@pytest.fixture(scope='module')
def app_with_temp_db():
    # Load our real environment variables
    load_dotenv(override=True)

    # Set new environment variable
    set_testing_db()   

    # Construct the new application
    application = app.create_app()

    app.add_item("testing")

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
    drop_db_collection()

def set_testing_db():    
    os.environ['AZ_MONGODB_DB_NAME'] = 'az-mongo-db-gcg-test'

def drop_db_collection():
    app.drop_collection()

@pytest.fixture(scope="module")
def driver():
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    with webdriver.Firefox(options=opts) as driver:
        yield driver

def test_task_journey(driver, app_with_temp_db):
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'
