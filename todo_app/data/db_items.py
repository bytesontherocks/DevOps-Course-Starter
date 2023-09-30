from flask import session
import pymongo
import os
from  todo_app.data.Item import Item

def getDb():
    client = pymongo.MongoClient(os.getenv('AZ_MONGODB_CONNECTION'))
    db = client[os.getenv('AZ_MONGODB_DB_NAME-db')]
    return db

def get_items():
    """
    Fetches items from the connected DB.

    Returns:
        list: The list of saved items.
    """     
    db = getDb()

    mdb_items_col = db.items
    mdb_items = mdb_items_col.find({})
    
    cards = []

    for it in mdb_items:
        cards.append(Item(it['id_short'], it['name'], it['status']))

    return cards

def add_item(title):
    """
    Adds a new item with the specified title to the connected database.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    db = getDb()

    mdb_items_col = db.items

    card = {
        "id_short": "", ## how to get/create that?
        "name": title,
        "status": "To Do"
    }

    post_id = mdb_items_col.insert_one(card).inserted_id

    return post_id

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
  

