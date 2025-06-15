# create_user_test.py
import sender_stand_request  # Para enviar solicitudes a la API
import data  # Para acceder al user_body base y headers
import random  # Se importa para generar datos únicos
import string  # Se importa para generar cadenas aleatorias (para emails únicos)


# Esta función se encarga de crear el cuerpo de la solicitud para el usuario.
# COPIA el user_body base de data.py y MODIFICA el campo 'firstName'.
# Esta función es crucial para la independencia de la prueba y la reutilización.
def get_user_body(first_name):
    # Copia el diccionario base de data.py para no modificar el original.
    current_body = data.user_body.copy()
    # Actualiza el campo 'firstName' con el valor proporcionado.
    # Convertimos first_name a string para evitar errores si se pasa un número o tipo diferente.
    current_body["firstName"] = str(first_name)

    # IMPORTANTE: Para asegurar que cada test sea independiente,
    # y para evitar errores de "usuario ya existe" o validaciones de unicidad,
    # generamos emails y números de teléfono únicos para CADA EJECUCIÓN.
    # Esto es CRÍTICO si la API valida la unicidad de email/phone.
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    # Aseguramos que first_name sea string antes de llamar a .lower()
    current_body["email"] = f"{str(first_name).lower()}_{random_suffix}@example.com"

    # Generación de número de teléfono más robusta
    # Intenta generar un número de 10 dígitos que comience con un dígito del 2 al 9
    # para cumplir con posibles validaciones de formatos comunes en Norteamérica.
    first_digit_phone = str(random.randint(2, 9))  # Asegura que el primer dígito no sea 0 o 1
    remaining_digits = ''.join(random.choices(string.digits, k=9))  # Los 9 dígitos restantes
    current_body["phone"] = f"+1{first_digit_phone}{remaining_digits}"

    # Retorna el diccionario modificado.
    return current_body


# Función para pruebas positivas de creación de usuario.
# Centraliza la lógica de envío de solicitud y aserciones comunes para escenarios exitosos.
def positive_assert(first_name):
    # 1. Preparar los datos de la solicitud:
    user_body = get_user_body(first_name)

    # 2. Enviar la solicitud POST para crear el usuario:
    user_response = sender_stand_request.post_new_user(user_body)

    # --- DEBUG INFO TEMPORAL (QUITAR DESPUÉS DE QUE EL TEST PASE) ---
    # print("\n--- DEBUG INFO: API Response ---")
    # print(f"Request Body Sent: {user_body}")
    # print(f"Response Status Code: {user_response.status_code}")
    # print(f"Response Text: {user_response.text}")
    # print("--- END DEBUG INFO: API Response ---\n")
    # --- FIN: DEBUG INFO TEMPORAL ---

    # 3. Aserciones de la respuesta de la API:
    # Comprueba que el código de estado HTTP de la respuesta sea 201 (Created).
    assert user_response.status_code == 201
    # Comprueba que la respuesta JSON contenga el campo "authToken" y que no esté vacío.
    assert user_response.json()["authToken"] != ""

    # 4. Verificación de la persistencia del usuario en la "tabla users":
    users_table_response = sender_stand_request.get_users_table()

    # --- DEBUG INFO TEMPORAL (QUITAR DESPUÉS DE QUE EL TEST PASE) ---
    # print("\n--- DEBUG INFO: USERS TABLE RESPONSE ---")
    # print(f"Users Table Status Code: {users_table_response.status_code}")
    # print(f"Users Table Content (Raw):\n{users_table_response.text}")
    # print("--- END DEBUG INFO: USERS TABLE RESPONSE ---\n")
    # --- FIN: DEBUG INFO TEMPORAL ---

    # Construye la cadena esperada de los datos del usuario, tal como aparecen DESPUÉS del ID
    # en una línea de la tabla CSV.
    # Formato de una línea de datos en la tabla (excluyendo el ID inicial):
    # firstName,phone,address,email,comment,authToken
    expected_user_data_in_line = (
            user_body["firstName"] + ","
            + user_body["phone"] + ","
            + user_body["address"] + ","
            + user_body["email"] + ","
            + ","  # Campo 'comment' que está vacío en la tabla
            + user_response.json()["authToken"]
    )

    # Manejo del carácter BOM (\ufeff): Este carácter puede estar al inicio del CSV y
    # puede causar problemas al buscar la cadena. Lo eliminamos.
    table_content_without_bom = users_table_response.text.lstrip('\ufeff')

    # --- DEBUG INFO TEMPORAL (QUITAR DESPUÉS DE QUE EL TEST PASE) ---
    # print(f"Expected user data in a table row (excluding ID): {expected_user_data_in_line}")
    # print(f"Content to search in (after BOM removal, first 200 chars):\n{table_content_without_bom[:200]}...")
    # --- FIN DEBUG INFO ---

    # Divide el contenido CSV en líneas y busca al usuario creado.
    found_user_count = 0
    lines = table_content_without_bom.strip().split('\n')
    data_lines = lines[1:]  # Salta la línea del encabezado

    for line in data_lines:
        first_comma_index = line.find(',')
        if first_comma_index != -1:
            line_data_without_id = line[first_comma_index + 1:]
            if expected_user_data_in_line in line_data_without_id:
                found_user_count += 1

    assert found_user_count == 1


# Función para pruebas negativas de creación de usuario con caracteres no válidos.
# first_name: El nombre de usuario que se enviará, el cual se espera que cause un error.
def negative_assert_symbol(first_name):
    # Obtiene una versión actualizada del cuerpo de solicitud de creación de un nuevo usuario o usuaria
    user_body = get_user_body(first_name)

    # Almacena el resultado de la solicitud
    user_response = sender_stand_request.post_new_user(user_body)

    # --- DEBUG INFO PARA NEGATIVE ASSERT ---
    print("\n--- DEBUG INFO: Negative API Response (Symbol) ---")
    print(f"Request Body Sent: {user_body}")
    print(f"Response Status Code: {user_response.status_code}")
    print(f"Response Text: {user_response.text}")
    print("--- END DEBUG INFO: Negative API Response (Symbol) ---\n")
    # --- FIN: DEBUG INFO PARA NEGATIVE ASSERT ---

    # Comprueba si la respuesta contiene el código 400
    assert user_response.status_code == 400

    # Comprueba si el atributo "code" en el cuerpo de respuesta es 400
    # Asume que el cuerpo de respuesta es un JSON con el campo "code".
    assert user_response.json()["code"] == 400

    # Comprueba si el atributo "message" en el cuerpo de la respuesta se ve así:
    # Se utiliza la concatenación de cadenas en Python para textos largos.
    assert user_response.json()["message"] == (
        "Has introducido un nombre de usuario no válido. "
        "El nombre solo puede contener letras del alfabeto latino, "
        "la longitud debe ser de 2 a 15 caracteres."
    )


# Función de prueba negativa cuando falta el campo 'firstName'.
# user_body: El cuerpo de la solicitud modificado (sin 'firstName').
def negative_assert_no_firstname(user_body):
    # Guarda el resultado de llamar a la función a la variable "response"
    user_response = sender_stand_request.post_new_user(user_body)

    # --- DEBUG INFO PARA NEGATIVE ASSERT (NO FIRST NAME) ---
    print("\n--- DEBUG INFO: Negative API Response (No First Name) ---")
    print(f"Request Body Sent: {user_body}")
    print(f"Response Status Code: {user_response.status_code}")
    print(f"Response Text: {user_response.text}")
    print("--- END DEBUG INFO: Negative API Response (No First Name) ---\n")
    # --- FIN: DEBUG INFO PARA NEGATIVE ASSERT ---

    # Comprueba si la respuesta contiene el código 400
    assert user_response.status_code == 400

    # Comprueba si el atributo "code" en el cuerpo de respuesta es 400
    assert user_response.json()["code"] == 400

    # Comprueba si el atributo "message" en el cuerpo de respuesta se ve así:
    assert user_response.json()["message"] == "No se han aprobado todos los parámetros requeridos"


# Prueba 1: Creación de un nuevo usuario con "firstName" de dos caracteres (prueba positiva).
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


# Prueba 2: Creación de un nuevo usuario con "firstName" de quince caracteres (prueba positiva).
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")  # "A" repetido 15 veces


# Prueba 3: Creación de un nuevo usuario con "firstName" de un solo carácter (prueba negativa).
# Se espera un error 400 con un mensaje específico.
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")


# Prueba 4: Creación de un nuevo usuario con "firstName" de dieciséis caracteres (prueba negativa).
# Se espera un error 400 con el mismo mensaje que para un carácter.
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("A" * 16)  # "A" repetido 16 veces


# Prueba 5: Creación de un nuevo usuario con un espacio en el nombre (prueba negativa).
# Se espera un error 400 con el mensaje de nombre de usuario no válido.
# Según las instrucciones, la API puede permitir espacios, pero la lista de comprobación no lo permite.
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aaa")


# Prueba 6: Creación de un nuevo usuario con símbolos especiales en el nombre (prueba negativa).
# Se espera un error 400 con el mensaje de nombre de usuario no válido.
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")  # Los símbolos especiales dentro del string


# Prueba 7: Creación de un nuevo usuario con un número en el nombre (prueba negativa).
# Se espera un error 400 con el mensaje de nombre de usuario no válido.
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")


# Prueba 8: Error cuando la solicitud no contiene el parámetro "firstName".
def test_create_user_no_first_name_get_error_response():
    # El diccionario con el cuerpo de la solicitud se copia del archivo "data" a la variable "user_body"
    user_body = data.user_body.copy()
    # El parámetro "firstName" se elimina de la solicitud
    user_body.pop("firstName")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)


# Prueba 9: Error cuando el parámetro "firstName" es una cadena vacía.
def test_create_user_empty_first_name_get_error_response():
    # El diccionario con el cuerpo de la solicitud se copia del archivo "data"
    user_body = data.user_body.copy()
    # Se establece el parámetro "firstName" como una cadena vacía
    user_body["firstName"] = ""
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)


# Prueba 10: Error cuando el tipo del parámetro "firstName" es un número.
def test_create_user_number_type_first_name_get_error_response():
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body(12)
    # El resultado de la solicitud para crear un nuevo usuario o usuaria se guarda en la variable response
    user_response = sender_stand_request.post_new_user(user_body)

    # Comprobar el código de estado de la respuesta
    assert user_response.status_code == 400
