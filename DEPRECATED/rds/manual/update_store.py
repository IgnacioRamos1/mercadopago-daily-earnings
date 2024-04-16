from sqlalchemy.orm import sessionmaker
import sys
import os
sys.path.append(os.path.abspath('..'))

from manual_migrate import migrate
from manual_store import Store
from utils.db_connection import dev_engine
from select_store import seleccionar_tienda
from utils.security import encrypt_string

Session = sessionmaker(bind=dev_engine)

def main():
    session = Session()

    # Se solicita el ID de la tienda una vez al principio
    store_id = seleccionar_tienda(session)
    print('---------------------------------')

    while True:
        choice = input("Do you want to update the access token of a store (1), update the owner of a store (2), or update the name of a store (3)? (q to quit): ")
        print('---------------------------------')

        if choice == '1':
            new_access_token = encrypt_string(input("Enter the new access token of the store: "))
            print('---------------------------------')

            store = session.query(Store).filter(Store.id == store_id).first()
            store.access_token = new_access_token
            session.commit()

            print(f"Store {store.name} access token updated successfully!")

        elif choice == '2':
            new_owner = input("Enter the new owner of the store: ")
            print('---------------------------------')

            store = session.query(Store).filter(Store.id == store_id).first()
            store.owner = new_owner
            session.commit()

            print(f"Store {store.name} owner updated successfully!")

        elif choice == '3':
            new_name = input("Enter the new name of the store: ")
            print('---------------------------------')

            store = session.query(Store).filter(Store.id == store_id).first()
            store.name = new_name
            session.commit()

            print(f"Store name updated successfully!")

        elif choice == 'q':
            break

        else:
            print("Please enter a valid option")
            print('---------------------------------')

    session.close()
    migrate()

if __name__ == '__main__':
    main()
