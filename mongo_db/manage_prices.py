from database import Database


def manage_product_prices(product):
    database = Database.get_instance()

    choice = input('Do you want to add a new price (1), update an existing one (2), or delete a price (3)? (q to quit): ')
    print('---------------------------------')

    while choice != 'q':
        if choice == '1':
            price = float(input('Enter the price of the product: '))
            print('---------------------------------')
            product['prices'].append(price)
            database.update_product(product['name'], product)
            print(f'Price {price} added successfully!')

        elif choice == '2':
            print('Current prices:')
            for i, price in enumerate(product['prices']):
                print(f'{i + 1}. {price}')
            print('---------------------------------')
            price_number = int(input('Enter the number of the price you want to update: '))
            print('---------------------------------')
            new_price = float(input('Enter the new price: '))
            print('---------------------------------')
            product['prices'][price_number - 1] = new_price
            database.update_product(product['name'], product)
            print(f'Price updated successfully!')

        elif choice == '3':
            print('Current prices:')
            for i, price in enumerate(product['prices']):
                print(f'{i + 1}. {price}')
            print('---------------------------------')
            price_number = int(input('Enter the number of the price you want to delete: '))
            print('---------------------------------')
            del product['prices'][price_number - 1]
            database.update_product(product['name'], product)
            print(f'Price deleted successfully!')

        else:
            print('Invalid choice!')

        choice = input('Do you want to add a new price (1), update an existing one (2), or delete a price (3)? (q to quit): ')
        print('---------------------------------')

