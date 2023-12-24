# Test project of a web application built with Flask and SQLite

## Introduction

This project is a web application built with Flask and SQLite. It provides a basic user authentication system, allowing users to register, log in, and manage their authentication keys. The application also includes API endpoints for managing keys and sending webhooks.

## Project Structure

The project structure is as follows:

- `app.py`: Defines the application's routes.
- `users/`: Contains the `login_user.py` and `register_user.py` files for handling user-related operations.
- `api/`: Contains the API endpoints for managing keys and sending webhooks.
- `index.html`: Defines the front-end of the application.
- `script.js`: Provides additional JavaScript functionality.
- `styles.css`: Contains the styling for the application.

## How to Run the Project

1. Ensure you have Python 3.8 or later installed on your machine.

2. Install the required Python packages by running the following command in your terminal:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Flask application:

    ```bash
    python app.py
    ```

    The application will start a server on `localhost:5000`. You can interact with the application by opening a web browser and navigating to [http://localhost:5000](http://localhost:5000).

Please note that the database is initialized and managed through the `DataManager` class in the `database.py` file. The `DataManager` class includes methods for creating and deleting authentication keys, checking user credentials, and more.
