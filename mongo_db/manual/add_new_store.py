from database import Database
from mongo_db.utils.security import encrypt_string

from datetime import datetime


def add_new_store():
    database = Database()

    choice = input('Do you want to add a new store (y/n)? ')

    while choice == 'y':
        store_name = input('Enter the name of the store: ')
        owner_name = input('Enter the name of the store owner: ')
        print('---------------------------------')
        access_token = encrypt_string(input('Enter the access token of the store: '))
        email = 'iramosibx@gmail.com'

        date = datetime.now().now()

        new_store = {
            'name': store_name,
            'owner': owner_name,
            'created_at': date,
            'access_token': access_token,
            'email': email,
            'products': [],
        }

        database.add_store(new_store)

        choice = input('Do you want to add a new store (y/n)? ')
        print('---------------------------------')


if __name__ == '__main__':
    add_new_store()  
