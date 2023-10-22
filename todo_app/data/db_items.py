from flask import session
import pymongo
import os
from  todo_app.data.Item import Item
from datetime import datetime


max_id = 0

def getDb():
    client = pymongo.MongoClient(os.getenv('AZ_MONGODB_CONNECTION'))
    db = client[os.getenv('AZ_MONGODB_DB_NAME')]
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

    global max_id

    for it in mdb_items:
        if int(it['id_short']) > max_id:
            max_id = int(it['id_short'])
        cards.append(Item(it['id_short'], it['name'], it['status']))

    print(f"max_id {max_id}")
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

    global max_id

    card = {
        "id_short": max_id + 1,
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
    db = getDb()

    mdb_items_col = db.items

    # print(f"id {card_short_id} :: current_status {current_list_name} :: new_status {new_list_name}")
    item = mdb_items_col.update_many({"id_short": card_short_id}, { "$set": { "status": new_list_name }})
    # print(current_list_name)
    # item = mdb_items_col.find_one({"id_short": 1})
    # print(item)
    # if item != None:
    #     newItem = { "$set": { "status": new_list_name } }
    #     resItem = mdb_items_col.update_one(item, newItem)
