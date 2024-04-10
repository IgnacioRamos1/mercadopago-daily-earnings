from sqlalchemy.orm import sessionmaker
from datetime import datetime

from manual_store import Store
from utils.db_connection import dev_engine
from utils.security import encrypt_string


Session = sessionmaker(bind=dev_engine)
session = Session()

choice = str(input("Do you want to add a new store? (y/n): "))

while choice != "y" and choice != "n":
    choice = str(input("Please enter a valid option (y/n): "))

while choice == "y":
    # Solicita los datos de la nueva tienda
    name = str(input("Enter the name of the store: "))
    access_token = encrypt_string(str(input("Enter the access token of the store: ")))
    email = "iramosibx@gmail.com"
    owner = str(input("Enter the owner of the store: "))

    # Agregar la fecha de creación de la tienda
    date = datetime.now().date()

    # Crea una nueva instancia de la clase Store con los datos proporcionados
    nueva_tienda = Store(
        name=name,
        access_token=access_token,
        email=email,
        created_at=date,
        owner=owner
    )

    # Agrega la nueva tienda a la sesión
    session.add(nueva_tienda)

    choice = str(input("Do you want to add another store? (y/n): "))

    while choice != "y" and choice != "n":
        choice = str(input("Please enter a valid option (y/n): "))

# Confirma las transacciones
session.commit()

# Cierra la sesión
session.close()
