import sys
import os
sys.path.append(os.path.abspath('..'))

from database import Database
from select_store import select_store
from select_product import select_product
from manage_prices import manage_product_prices


def add_new_product(database):
    store = select_store()

    choice = input('Do you want to add a new product (1), update an existing one (2), or delete a product (3)? (q to quit): ')
    print('---------------------------------')

    while choice != 'q':
        if choice == '1':
            name = input('Enter the name of the product: ')
            print('---------------------------------')
            
            prices = []
            price = float(input('Enter the price of the product: '))
            print('---------------------------------')
            prices.append(price)
            
            multiple_prices = input('Do you want to add more prices? (y/n): ')
            print('---------------------------------')
            while multiple_prices.lower() == 'y':
                price = float(input('Enter the price of the product: '))
                prices.append(price)
                print('---------------------------------')
                multiple_prices = input('Do you want to add more prices? (y/n): ')
                print('---------------------------------')

            
            new_product = {
                'name': name,
                'prices': prices
            }

            database.add_product(store['_id'], new_product)

        elif choice == '2':
            product = select_product(store['_id'])
            print('---------------------------------')

            if product:
                print(f'You have selected: {product["name"]}')
                print('---------------------------------')
                manage_product_prices(product)
            else:
                print('Product not found or not selected.')

        elif choice == '3':
            product = select_product(store['_id'])
            print('---------------------------------')

            if product:
                confirm = input(f'Are you sure you want to delete {product["name"]} and all its prices? (y/n): ')
                print('---------------------------------')
                if confirm.lower() == 'y':
                    database.delete_product(store['_id'], product['name'])
                    print(f'Product {product["name"]} deleted successfully!')
                
                else:
                    print('Product not found or not selected.')


        else:
            print('Invalid option. Please try again.')

        choice = input('Do you want to add a new product (1), update an existing one (2), or delete a product (3)? (q to quit): ')
        print('---------------------------------')
    


if __name__ == '__main__':
    database = Database.get_instance()
    add_new_product(database)
    database.close_connection()

