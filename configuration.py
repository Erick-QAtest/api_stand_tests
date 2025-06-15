

# configuration.py

# URL base del servicio de Tripleten
URL_SERVICE = "https://cnt-7e5ce5db-3bcc-471f-af2c-39f05603d0e2.containerhub.tripleten-services.com"

# Rutas específicas de los endpoints
DOC_PATH = "/docs"
LOG_MAIN_PATH = "/api/logs/main/"
USERS_TABLE_PATH = "/api/db/resources/user_model.csv"  # Ruta para obtener la tabla de usuarios (CSV)
CREATE_USER_PATH = "/api/v1/users/"                 # Ruta para crear un nuevo usuario (POST)
PRODUCTS_KITS_PATH = "/api/v1/products/kits/"