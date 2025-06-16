🧪 API Testing Automation for User Creation 🧪
This project contains a set of automated tests in Python to verify the user creation functionality of an API. It follows best practices principles of automation, such as unit of testing, data independence, and test autonomy.

🎯 Project Objective
The main objective is to ensure the correct creation of users through the API, verifying both successful scenarios (positive tests) and error scenarios (negative tests) based on the requirements of a specific checklist.

🚀 Setup and Installation
To set up and run this project in your local environment, follow these steps:

Clone the Repository:
If you haven't already, clone this Git repository to your local machine.

git clone https://github.com/Erick-QAtest/api_stand_tests # Make sure to change this to your repository URL!
cd your_repo

Create and Activate a Virtual Environment:
It's good practice to use virtual environments to isolate project dependencies.

python3 -m venv .venv
# For macOS/Linux:
source .venv/bin/activate
# For Windows (Command Prompt):
.venv\Scripts\activate.bat
# For Windows (PowerShell):
.venv\Scripts\Activate.ps1

Install Dependencies:
Install the necessary libraries (mainly requests for HTTP requests and pytest for the testing framework).

pip install requests pytest

📂 Project Structure
The project is organized as follows:

api_stand_tests/ (Project root folder)

.venv/ (Python virtual environment)

configuration.py: Contains the base URLs and API endpoint paths. Make sure to keep URL_SERVICE updated!

data.py: Defines common HTTP headers (headers) and the base request body for user creation (user_body).

sender_stand_request.py: Module containing functions to send HTTP requests to the API (POST for user creation, GET for fetching the users table).

create_user_test.py: Contains all automated test functions.

🧪 How to Run Tests
To run all automated tests in the project:

Ensure your virtual environment is activated.

Navigate to your project's root directory (api_stand_tests) in your terminal.

Run Pytest:

pytest

Pytest will automatically discover and execute all test functions defined in create_user_test.py. You will see a summary of the results (PASSED, FAILED).

🧠 Assertion Logic
To optimize and reuse test code, specialized assertion functions have been implemented:

positive_assert(first_name):

Purpose: Encapsulates the verification logic for successful user creation scenarios.

Actions: Sends a POST request to create a user, verifies that the status code is 201 (Created), that the response contains a non-empty authToken, and that the user has been correctly persisted in the "users table".

Usage: Called in tests where user creation is expected to be successful.

negative_assert_symbol(first_name):

Purpose: Encapsulates the verification logic for error scenarios related to invalid first_name format or content.

Actions: Sends a POST request with an invalid first_name, verifies that the status code is 400 (Bad Request), that the error code in the JSON response is 400, and that the error message matches a specific message about an invalid username.

Usage: Called in tests where the API is expected to reject user creation due to an incorrectly formatted first_name (e.g., symbols, numbers, invalid length).

negative_assert_no_firstname(user_body):

Purpose: Encapsulates the verification logic for error scenarios where the firstName field is missing or empty in the request.

Actions: Sends a POST request with a user_body missing the firstName field or with an empty firstName, verifies that the status code is 400 (Bad Request), that the error code in the JSON response is 400, and that the error message indicates missing required parameters.

Usage: Called in tests where the API is expected to reject user creation due to the absence or invalidity of the firstName field as a required parameter.

📋 Implemented Test Cases
Currently, the project includes the following tests for user creation:

test_create_user_2_letter_in_first_name_get_success_response():

Scenario: firstName with 2 letters (e.g., "Aa").

Type: Positive (expects 201 Created).

test_create_user_15_letter_in_first_name_get_success_response():

Scenario: firstName with 15 letters (e.g., "Aaaaaaaaaaaaaaa").

Type: Positive (expects 201 Created).

test_create_user_1_letter_in_first_name_get_error_response():

Scenario: firstName with 1 letter (e.g., "A").

Type: Negative (expects 400 Bad Request - invalid name).

test_create_user_16_letter_in_first_name_get_error_response():

Scenario: firstName with 16 letters (e.g., "AAAAAAAAAAAAAAAA").

Type: Negative (expects 400 Bad Request - invalid name).

test_create_user_has_space_in_first_name_get_error_response():

Scenario: firstName with a space (e.g., "A Aaa").

Type: Negative (expects 400 Bad Request - invalid name).

Note: This test currently fails because the API allows spaces, contrary to the checklist's expectation.

test_create_user_has_special_symbol_in_first_name_get_error_response():

Scenario: firstName with special symbols (e.g., "№%@",).

Type: Negative (expects 400 Bad Request - invalid name).

test_create_user_has_number_in_first_name_get_error_response():

Scenario: firstName with numbers (e.g., "123").

Type: Negative (expects 400 Bad Request - invalid name).

test_create_user_no_first_name_get_error_response():

Scenario: Request without the firstName field.

Type: Negative (expects 400 Bad Request - required parameters).

test_create_user_empty_first_name_get_error_response():

Scenario: firstName as an empty string (e.g., "").

Type: Negative (expects 400 Bad Request - required parameters).

test_create_user_number_type_first_name_get_error_response():

Scenario: firstName as a number type (e.g., 12).

Type: Negative (expects 400 Bad Request - type error).

## Última Actualización

Este proyecto se actualizó el 16 de junio de 2025 con nuevos cambios.