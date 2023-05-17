from flask import session
import requests
import json
import os
from  todo_app.data.Item import Item

headers = {
  "Accept": "application/json"
}

query = {
  'key': os.getenv('TRELLO_API_KEY'),
  'token': os.getenv('TRELLO_API_TOKEN')
}

def _get_list_id(list_name):
    trello_board = os.getenv('TRELLO_BOARD_ID')
    url = f"https://api.trello.com/1/boards/{trello_board}/lists"

    response = requests.get(
        url,
        headers=headers,
        params=query)

    list_id = ""

    if response.status_code == 200:
        lists = response.json()

        for l in lists:
            if l['name'] == list_name:
                list_id = l['id']
    else:
        print(f"_get_list_id request has failed. Status code: {response.status_code}")

    return list_id

def _get_cards():
    trello_board = os.getenv('TRELLO_BOARD_ID')
    url = f"https://api.trello.com/1/boards/{trello_board}/lists"
    
    query['cards'] = 'open'

    response = requests.get(
        url,
        headers=headers,
        params=query)

    items = []
    
    if response.status_code == 200:
        lists = response.json()

        for list in lists:
            cards = list['cards']
            for c in cards:
                items.append(Item(c['idShort'], c['name'], list['name']))
    else:
        print(f"_get_cards_in_list request has failed. Status code: {response.status_code}")
    
    return items

def _get_card_id(list_id, id_short : int):
    
    url = f"https://api.trello.com/1/lists/{list_id}/cards"

    response = requests.get(
        url,
        headers=headers,
        params=query)

    if response.status_code == 200:
        cards = response.json()
       
        for c in cards:
            if c['idShort'] == id_short:
                return c['id']
    else:
        print(f"_get_card_id request has failed. Status code: {response.status_code}")
    
    return ""

def _add_card(list_id, card_name):

    url = "https://api.trello.com/1/cards"

    query['name'] = card_name
    query['idList'] = list_id

    response = requests.post(
        url,
        headers=headers,
        params=query
    )

    #print(response.request.url)
    #print(response.request.body)
    #print(response.request.headers)

def get_items():
    """
    Fetches items from the Trello API.

    Returns:
        list: The list of saved items.
    """     
    return _get_cards()

def add_item(title):
    """
    Adds a new item with the specified title to the Trello board.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    todo_list_id = _get_list_id("To Do")
    _add_card(todo_list_id, title)

def move_card_to_new_list(card_short_id, current_list_name, new_list_name):
    """
    Moves an specific card from one list to another

    Args:
        card_short_id: short id of the card to move e.g. 14
        current_list_name: name of the list that the card to move belongs to 'To Do'
        new_list_name: name of the list that the card to move needs be moving to 'Done'

    Returns:
        item: void
    """
    current_list_id = _get_list_id(current_list_name)
    new_list_id = _get_list_id(new_list_name)    
    card_id = _get_card_id(current_list_id, card_short_id)

    if current_list_id == "" or new_list_id == "" or card_id == "":
        print(f"card_short_id: {card_short_id}")
        print(f"current_list_name: {current_list_name}")
        print(f"new_list_name: {new_list_name}")
        print("Movement not allowed. Only from Status 'To Do' to 'Done' or vice versa. Check item status!")

    else: 
        url = f"https://api.trello.com/1/cards/{card_id}"

        # add destination list
        query['idList'] = new_list_id
        
        response = requests.put(
            url,
            headers=headers,
            params=query
        )

        if response.status_code == 200:
            print("card moved successfully")
        else:
            print("Error moving card")
