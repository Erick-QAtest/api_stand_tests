# sender_stand_request.py
import requests       # Para realizar solicitudes HTTP
import configuration  # Para obtener las URLs y rutas de los endpoints
import data           # Para obtener los headers de las solicitudes

# Función para enviar una solicitud POST para crear un nuevo usuario
# body: Diccionario con los datos del usuario a crear
def post_new_user(body):
    return requests.post(
        url=configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
        json=body,          # Envía el diccionario 'body' como JSON en la solicitud
        headers=data.headers # Usa los headers definidos en data.py (ej. Content-Type)
    )

# Función para enviar una solicitud GET para obtener los datos de la tabla de usuarios
# Asume que la respuesta es texto plano, posiblemente CSV.
def get_users_table():
    return requests.get(
        url=configuration.URL_SERVICE + configuration.USERS_TABLE_PATH
    )
