import sys
import os
sys.path.append(os.path.abspath('..'))


from database import Database
from select_store import select_store


def delete_store():
    database = Database()

    store = select_store()

    choice = input(f'Are you sure you want to delete the store {store["name"]}? (y/n): ')

    if choice == 'y':
        database.delete_store(store['_id'])

    database.close_connection()


if __name__ == '__main__':
    delete_store()
