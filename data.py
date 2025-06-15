# data.py
import random  # Necesario para generar números aleatorios para el teléfono
import string  # Puede ser útil para otros campos, no estrictamente para el teléfono ahora

headers = {
    "Content-Type": "application/json"
}

# Diccionario base para el cuerpo de la solicitud de creación de usuario.
# La función get_user_body en create_user_test.py lo copiará y modificará el "firstName".
# ES FUNDAMENTAL que este diccionario contenga TODOS los campos requeridos por la API
# para crear un usuario, con valores por defecto válidos.
user_body = {
    "firstName": "Default",
    "lastName": "User",
    # *** CAMBIO AQUÍ: Genera un número de teléfono más adecuado y único ***
    # El formato "+[país][número de 10 dígitos]" es común.
    # Usamos random.randint para asegurar que sea diferente en cada ejecución.
    "phone": f"+1{random.randint(1000000000, 9999999999)}", # Ejemplo: +1 seguido de 10 dígitos
    "address": "123 Elm Street, Hilltop",
    "email": f"default.user.{random.randint(1, 10000)}@example.com", # Asegura que el email también sea único
    "password": "Password123!"
}

product_ids = {
    "ids": [1, 2, 3]
}

# La función get_user_body ya no está aquí, está en create_user_test.py