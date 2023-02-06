from flask import session
import requests
import json
import os

trello_api = os.getenv('TRELLO_API_KEY')
trello_token = os.getenv('TRELLO_API_TOKEN')
trello_board = os.getenv('TRELLO_BOARD_ID')

headers = {
  "Accept": "application/json"
}

query = {
  'key': trello_api,
  'token': trello_token
}

def get_lists():
    
    url = f"https://api.trello.com/1/boards/{trello_board}/lists"

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query)

    names = []

    if response.status_code == 200:
        lists = json.loads(response.text)
        for l in lists:
            names.append(l['name'])
            print(f"List id{l['id']} and name {l['name']}")
    
    return names 

def get_list_id(list_name):

    url = f"https://api.trello.com/1/boards/{trello_board}/lists"

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query)

    todo_list_id = ""

    if response.status_code == 200:
        lists = json.loads(response.text)

        for l in lists:
            if l['name'] == list_name:
                todo_list_id = l['id']
    else:
        print(f"get_list_id request has failed. Status code: {response.status_code}")

    return todo_list_id

def get_cards_in_list(list_id, list_name):
    
    url = f"https://api.trello.com/1/lists/{list_id}/cards"

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query)

    items = []
    
    if response.status_code == 200:
        cards = json.loads(response.text)
       
        #print(cards)
        for c in cards:
            item = {'id': c['idShort'], 'status': list_name, 'title': c['name']}
            items.append(item)        
    else:
        print(f"get_cards_in_list request has failed. Status code: {response.status_code}")
    
    return items

def get_card_id(list_id, id_short : int):
    
    url = f"https://api.trello.com/1/lists/{list_id}/cards"

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query)

    items = []
    
    if response.status_code == 200:
        cards = json.loads(response.text)
       
        for c in cards:
            if c['idShort'] == id_short:
                return c['id']
    else:
        print(f"get_card_id request has failed. Status code: {response.status_code}")
    
    return ""

def move_card_to_new_list(old_list_id, new_list_id, card_short_id):
    
    card_id = get_card_id(old_list_id, card_short_id)

    url = f"https://api.trello.com/1/cards/{card_id}"
    
    query = {
        'idList': new_list_id,
        'key': trello_api,
        'token': trello_token
    }

    print(f"moving card with Short ID {card_short_id} and long id {card_id} from old list id {old_list_id} to new list id {new_list_id}")

    response = requests.request(
        "PUT",
        url,
        headers=headers,
        params=query
    )


def add_card(list_id, card_name):
    url = "https://api.trello.com/1/cards"

    query = {
        'idList': list_id,
        'name' : card_name,
        'key': trello_api,
        'token': trello_token
    }

    response = requests.request(
        "POST",
        url,
        headers=headers,
        params=query
    )

    print(response.request.url)
    print(response.request.body)
    print(response.request.headers)

def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    #get_lists()
    all_items = []
    lists_names = get_lists()

    for n in lists_names:
        cards = get_cards_in_list(get_list_id(n),n)
        for c in cards:
            all_items.append(c)

     # Testing+
    todo_list_id = get_list_id("To Do")
    pm_list_id = get_list_id("from_postman")

    move_card_to_new_list(todo_list_id, pm_list_id, 7)
    #
    return  all_items


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    todo_list_id = get_list_id("To Do")
    add_card(todo_list_id, title)


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item
