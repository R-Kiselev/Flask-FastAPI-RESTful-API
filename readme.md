# Flask-FastAPI-restful API

This project implements RESTful API for a simple banking system. 
Inspired by the structure and some solutions from the [cookiecutter-flask-restful](https://github.com/karec/cookiecutter-flask-restful) project.

## Features

### BankService

* Simple flask application using application factory, blueprints
* Simple pagination utils
* Simple cli implementation with basics commands (init, run, etc.)
* [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/) included in entry point
* RBAC using [Flask-JWT-Extended](http://flask-jwt-extended.readthedocs.io/en/latest/) 
* Configuration using environment variables
* Different environment files for local and docker development (.env and .dockerenv files)
* Docker-compose configuration for running the application in a containerized environment
* Simple sync message queue client(producer) that sends messages to the queue

### LogService

* Simple FastAPI async application
* Simple pagination utils
* Async message queue server(consumer) that listens to the queue and saves logs to the mongodb
* Docker-compose configuration for running the application in a containerized environment
* Different environment files for local and docker development (.env and .dockerenv files)

### EmailService

* Simple FastAPI async application
* Sending email using aiosmtplib
* Async message queue server(consumer) that listens to the queue and sends emails
* Docker-compose configuration for running the application in a containerized environment
* Different environment files for local and docker development (.env and .dockerenv files)

## Main libraries used

### BankService

* [Flask](http://flask.pocoo.org/)
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/) 
* [Marshmallow](https://marshmallow.readthedocs.io/en/stable/index.html)
* [Flask-JWT-Extended](http://flask-jwt-extended.readthedocs.io/en/latest/)
* [dotenv](https://github.com/theskumar/python-dotenv)
* [pika](https://pika.readthedocs.io/en/stable/)
* [requests](https://requests.readthedocs.io/en/master/)

### LogService

* [FastAPI](https://fastapi.tiangolo.com/)
* [Pydantic](https://pydantic-docs.helpmanual.io/)
* [AsyncIO](https://docs.python.org/3/library/asyncio.html)
* [Motor](https://motor.readthedocs.io/en/stable/)
* [aio_pika](https://aio-pika.readthedocs.io/en/latest/)

### EmailService

* [FastAPI](https://fastapi.tiangolo.com/)
* [Pydantic](https://pydantic-docs.helpmanual.io/)
* [AsyncIO](https://docs.python.org/3/library/asyncio.html)
* [aiosmtplib](https://aiosmtplib.readthedocs.io/en/latest/)
* [aio_pika](https://aio-pika.readthedocs.io/en/latest/)

## Usage

* [Project structure](#Project-structure)
* [Installation](#Installation)
* [Configuration](#Configuration)
* [Authentication](#Authentication)
* [Using docker-compose](#using-docker-compose)
* [Makefile](#makefile-usage)
* [CRUD operations examples](#CRUD-operations-examples)
* [RabbitMQ usage](#RabbitMQ-usage)

## Project structure

### BankService
    ```
    .
    │
    ├── app/                   
    │   ├── api/
    │   │   ├── resources/
    │   │   │   ├── accounts.py
    │   │   │   ├── ...
    │   │   ├── schemas/
    │   │   │   ├── account.py
    │   │   │   ├── ...
    │   │   └── views.py
    │   ├── auth/
    │   │   ├── utils.py
    │   │   └── views.py 
    │   ├── commons/
    │   │   ├── base_resources.py
    │   │   ├── validation_utils.py
    │   │   └── pagination.py
    │   ├── models/
    │   │   ├── account.py
    │   │   ├── ...
    │   │── app.py
    │   │── config.py
    │   │── error_handling.py
    │   │── extensions.py
    │   │── message_queue.py
    │   │── wsgi.py
    │   └── flask_cli.py
    ├── requirements.txt
    ├── Dockerfile
    ├── .dockerignore
    ├── entrypoint.sh
    ├── .dockerenv
    └── .env
    ```

- **app/** ── Root directory for the Flask application code.
  - **api/** ── Defines API logic and structure.
    - **resources/** ── Contains RESTful resources for different API endpoints.
    - **schemas/** ── Contains Marshmallow schemas for data serialization and validation.
    - **views.py** ── Registers API blueprint and endpoint routes.
  - **auth/** ── Manages authentication and authorization logic.
    - **utils.py** ── Contains utility functions for RBAC and JWT handling.
    - **views.py** ── Registers `auth` blueprint and endpoint routes related to authentication.
  - **commons/** ── Holds reusable utilities and shared components.
    - **base_resources.py** ── Provides base classes for API resources.
    - **validation_utils.py** ── Includes helper functions for data validation.
    - **pagination.py** ── Implements pagination utilities for API responses.
  - **models/** ── Defines database models for application entities.
  - **app.py** ── Implements the Flask application factory and initializes the app.
  - **config.py** ── Contains configuration settings for different flask environments.
  - **error_handling.py** ── Manages Flask app error handling and logs exceptions.
  - **extensions.py** ── Initializes and configures Flask extensions (e.g., SQLAlchemy, Marshmallow) and other services.
  - **flask_cli.py** ── Defines custom Flask CLI commands for tasks like app init.
  - **wsgi.py** ── Entry point for running the Flask application.
  - **message_queue.py** ── Contains message queue client for sending\retreiveing messages to the queue.
- **requirements.txt** ── Lists Python dependencies required for the project.
- **.env** ── Configuration file for local development.
- **.dockerenv** ── Configuration file for docker development.
- **.dockerignore** ── Specifies files and directories to exclude when building Docker images.
- **Dockerfile** ── Defines the application container image.
- **entrypoint.sh** ── Contains the entrypoint script for the Docker container.

### LogService

    ```
    .
    │
    ├── app/                   
    │   ├── rabbitmq/
    │   │   ├── connection_manager.py
    │   │   ├── message_queue.py
    │   │   └── run_manager.py
    │   ├── resources/
    │   │   └── logs.py 
    │   ├── schemas/
    │   │   └── logs.py
    │   │── config.py
    │   │── db.py
    │   │── logging.py
    │   │── main.py
    │   └── pagination.py
    ├── .dockerenv
    ├── .dockerignore
    ├── .env
    ├── .dockerenv
    ├── Dockerfile
    ├── cert.pem
    ├── key.pem
    ├── entrypoint.sh
    └── requirements.txt
    ```


- **app/** ── Root directory for the FastAPI application code.
  - **rabbitmq/** ── Contains RabbitMQ server logic for listening to the queue and saving logs to the MongoDB.
    - **connection_manager.py** ── Manages RabbitMQ connection and channel. Include reconnect logic.
    - **message_queue.py** ── Contains message queue server for retreiveing messages from the queue and saving messages.
    - **run_manager.py** ── Manages RabbitMQ server, creates background task for listening to the queue.
  - **resources/** ── Defines FastAPI resources for different API endpoints. Contains API routers to separate routing logic.
    - **logs.py** ── Defines CRUD operations for logs.
  - **schemas/** ── Contains Pydantic schemas for data serialization and validation.
    - **logs.py** ── Defines Pydantic schema for log message.
  - **config.py** ── Contains configuration settings for application. Using pydantic BaseSettings for environment variables.
  - **db.py** ── Init and close MongoDB connection on startup and shutdown. Provides functionality for getting MongoDB client.
  - **logging.py** ── Contains logging configuration for the application. Handles logging to the console and file.
  - **main.py** ── Entry point for running the FastAPI application. Using application factory pattern.
  - **pagination.py** ── Simple pagination utilities for API responses.
- **requirements.txt** ── Lists Python dependencies required for the project.
- **.env** ── Configuration file for local development.
- **.dockerenv** ── Configuration file for docker development.
- **.dockerignore** ── Specifies files and directories to exclude when building Docker images.
- **Dockerfile** ── Defines the application container image.
- **entrypoint.sh** ── Contains the entrypoint script for the Docker container.
- **cert.pem** ── Self-signed SSL certificate for the FastAPI application. Used for HTTPS connection.
- **key.pem** ── Private key for the SSL certificate. Used for HTTPS connection.

### EmailService

    ```
    .
    │
    ├── app/                   
    │   ├── rabbitmq/
    │   │   ├── connection_manager.py
    │   │   ├── message_queue.py
    │   │   └── run_manager.py
    │   │── config.py
    │   │── email_sender.py
    │   │── main.py
    │   └── logging.py
    ├── .dockerenv
    ├── .dockerignore
    ├── .env
    ├── .dockerenv
    ├── Dockerfile
    ├── cert.pem
    ├── key.pem
    ├── entrypoint.sh
    └── requirements.txt
    ```

- **app/** ── Root directory for the FastAPI application code.
    - **rabbitmq/** ── Contains RabbitMQ server logic for listening to the queue and sending emails.
        - **connection_manager.py** ── Manages RabbitMQ connection and channel. Include reconnect logic.
        - **message_queue.py** ── Contains message queue server for retreiveing messages from the queue and sending emails.
        - **run_manager.py** ── Manages RabbitMQ server, creates background task for listening to the queue.
    - **config.py** ── Contains configuration settings for application. Using pydantic BaseSettings for environment variables.
    - **email_sender.py** ── Contains email sender logic. Uses aiosmtplib to send emails asynchronously.
    - **main.py** ── Entry point for running the FastAPI application. Using application factory pattern.
    - **logging.py** ── Contains logging configuration for the application. Handles logging to the console and file.
- **requirements.txt** ── Lists Python dependencies required for the project.
- **.env** ── Configuration file for local development.
- **.dockerenv** ── Configuration file for docker development.
- **.dockerignore** ── Specifies files and directories to exclude when building Docker images.
- **Dockerfile** ── Defines the application container image.
- **entrypoint.sh** ── Contains the entrypoint script for the Docker container.
- **cert.pem** ── Self-signed SSL certificate for the FastAPI application. Used for HTTPS connection.
- **key.pem** ── Private key for the SSL certificate. Used for HTTPS connection.


## Installation

### RabbitMQ
1. Install RabbitMQ on your computer.
2. Create a new user and virtual host.

### BankService
1. Clone repository.
2. Create python venv
3. pip install -r requirements.txt
4. Init MySQL database on your computer.
5. Configure .env or .dockerenv file

### LogService
1. Clone repository.
2. Create python venv
3. pip install -r requirements.txt
4. start MongoDB database on your computer.
5. Configure .env or .dockerenv file

### EmailService
1. Clone repository.
2. Create python venv
3. pip install -r requirements.txt
4. Configure .env or .dockerenv file


## Configuration
Configuration is handled by environment variables, for local development purpose you just need to create and add entries in `.env` file.

If you want to run the application in a containerized environment, you should create a `.dockerenv` file 
and change connection URI host from `localhost` to `service_name` (e.g., `db`).

### BankService

```env
FLASK_ENV = 'development'
FLASK_APP = 'app.app:create_app'
FLASK_CERT = 'adhoc'
SECRET_KEY = 'SECRET'
JWT_SECRET_KEY = "JWT_SECRET"

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:pass@localhost:3306/mybank'

RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = "5672"

DEFAULT_ROLE = 'user'

ADMIN_EMAIL = 'admin@gmail.com'
ADMIN_PASS = 'password'

LOG_SERVICE_URL = "https://localhost:8000"
CALLBACK_QUEUE = "doesnt_matter"
```
`FLASK_ENV` is set to `development` by default. This automatically enables debug mode and changes errorhandlers behavior (look at `config.py`).

### LogService

```env
MONGODB_URI="mongodb://localhost:27017"
MONGODB_NAME="log-service"
MONGODB_COLLECTIONS="logs"

AMQP_URI = "amqp://guest:guest@localhost:5672/"
QUEUE_NAME = "log-service"
EXCHANGE_NAME = "topic_exchange"
ROUTING_KEY = "account.created"
```

### EmailService

```env
AMQP_URI = "amqp://guest:guest@localhost:5672/"
QUEUE_NAME = "email-service"
EXCHANGE_NAME = "topic_exchange"
ROUTING_KEY = "*.created"

email_port = "465"  # SMTP SSL Port (ex. 465)
email_host = "smtp.gmail.com"  # SMTP host (ex. smtp.gmail.com)
email_user = "your_address@gmail.com"  # SMTP Login credentials
email_app_password = "abcd abcd abcd abcd"  # SMTP Login credentials. Look at this [article](https://support.google.com/accounts/answer/185833?hl=en)

email_receivers =  "test@gmail.com, example@gmail.com" # Receivers, can be multiple. Configured here for convenience.
email_subject = "Message from Bank service" 
```

## Authentication

### Registration

POST https://localhost:5000/auth/register

HEADERS
```json
{
    Content-Type: application/json
}
```

REQUEST
```json
{
    "email" : "exampleuser@gmail.com",
    "password" : "password"
}
```

RESPONSE
```json
201 CREATED
{
    "item": {
        "blocked_on": null,
        "email": "exampleuser@gmail.com",
        "id": 2,
        "is_blocked": false,
        "last_login_date": null,
        "registered_on": "2025-01-16T17:10:26",
        "roles": [
            "user"
        ]
    },
    "msg": "item created"
}
```

### Login

To access protected resources, you will need an access token. You can generate an access and token using `/auth/login` endpoint. 
Created access token contains client id, account id's in jwt claims if they exists.

POST https://localhost:5000/auth/login

HEADERS
```json
{
    Content-Type: application/json
}
```

REQUEST
```json
{
    "email" : "admin@gmail.com",
    "password" : "password"
}
```

RESPONSE
```json
200 OK
{
    "access_token": {your_token}
}
```

## Using docker-compose

You can use docker-compose to run the application in a containerized environment.
You should create `.dockerenv` file for running application. Look at [configuration](#configuration) section for more details.
Also, you can use the Makefile to automate repetitive tasks.
At first, you need to initialize your environment by running the following commands. 
This will create containers and initialize the database.

With docker-compose
```bash
docker-compose build
docker-compose up
docker exec -it <backend_container_id> flask db-init
docker exec -it <backend_container_id> flask db-migrate
docker exec -it <backend_container_id> flask db-upgrade
docker exec -it <backend_container_id> flask init
```

With docker-compose and the Makefile
```bash
make init
```

Now your project is ready to use.

## Makefile usage

Initizalize the environment
```bash
make init
```

Build the containers
```bash
make build
```

Rebuild the containers: Drop, build and run the containers.
```bash
make rebuild
```

Run the containers
```bash
make run
```

Create migrations folder
```bash
make db-init
```

Create new database migration
```bash
make db-migrate
```

Apply database migrations
```bash
make db-upgrade
```

## CRUD operations examples

If user don't have access to endpoint, he will receive 403 Forbidden status code.
This can be caused by :
* trying to access endpoint without token
* if user has wrong role
* if user is not owner of the resource

RESPONSE
```json
403 Forbidden
{
    "msg": "Access denied"
}
```

GET https://localhost:5000/api/accounts/1/cards

HEADERS
```json
{
    Authorization : Bearer {{token}}
}
```

RESPONSE
```json
200 OK
{
    "total": 4,
    "pages": 1,
    "next": "/api/accounts/1/cards?page_number=1&page_size=5",
    "prev": "/api/accounts/1/cards?page_number=1&page_size=5",
    "results": [
        {
            "id": 1,
            "balance": 300,
            "account_id": 1
        },
        {
            "id": 2,
            "balance": 500,
            "account_id": 1
        },
        {
            "id": 5,
            "balance": 500,
            "account_id": 1
        },
        {
            "id": 7,
            "balance": 500,
            "account_id": 1
        }
    ]
}
```
POST https://localhost:5000/api/accounts/1/cards

HEADERS
```json
{
    Authorization : Bearer {{token}}
}
```

REQUEST
```json
{
    "balance" : 520
}
```

RESPONSE
```json
201 CREATED
{
    "msg": "item created",
    "item": {
        "id": 8,
        "balance": 520,
        "account_id": 1
    }
}
```

PUT https://localhost:5000/api/accounts/cards/1

HEADERS
```json
{
    Content-Type : application/json,
    Authorization : Bearer {{token}}
}
```

REQUEST
```json
{
    "balance" : 600
}
```

RESPONSE
```json
200 OK
{
    "msg": "item updated",
    "item": {
        "id": 1,
        "balance": 600,
        "account_id": 1
    }
}
```
DELETE https://localhost:5000/api/accounts/cards/1

HEADERS
```json
{
    Authorization : Bearer {{token}}
}
```

RESPONSE
```json
200 OK
{
    "msg": "item deleted",
    "item": {
        "id": 1,
        "balance": 600,
        "account_id": 1
    }
}
```

Other resources are similar to Cards endpoints.

## RabbitMQ usage

#### BankService

The message queue client is initialized within the `extensions.py` file upon application startup. 
Due to the infrequent use of the message queue within the BankService, the connection and channel are established and closed for each message sending operation. 

#### Message Sending Scenarios:

- Account Creation:
    - Routing Key: `account.created`
    - Trigger: Whenever a new user account is created within the BankService.
    - Action: BankService publishes a message to the message broker (RabbitMQ).
    - Consumers:
        - EmailService: Consumes this message and sends an email notification
        - LogService: Consumes this message and persists it as a log entry in the database.
 - Bank Creation:
    - Routing Key: `bank.created`
    - Trigger: Whenever a new Bank entity is created within the BankService.
    - Action: BankService publishes a message to the message broker (RabbitMQ).
    - Consumers:
        - EmailService: Consumes this message.
            - Step 1: Sends an email notification.
            - Step 2: Acknowledgment: Sends an ACK message back to the message broker. Sends a message into message queue, declared in the bank service.
    - BankService (ACK Handling):
        - Trigger: BankService listens for and receives the acknowledgment (ACK) message sent by EmailService.
        - Action: Upon receiving the ACK, BankService makes an HTTP request to the LogService. This ensures that the logging only occurs after successful email confirmation.

#### Key Considerations & Design Choices:

- Message Acknowledgments (ACKs): The use of acknowledgments in the Bank Creation scenario ensures that the LogService only logs the event after the EmailService has successfully sent the email notification.

- Exchange and Routing Keys: 
    - Project uses a `topic exchange` with different routing keys for each event type (`account.created`, `bank.created`).
    - LogService gets messages with `account.created` routing key.
    - EmailService gets messages with `*.created` routing keys.

- Message Format: Explicitly defining the message format (e.g., JSON) ensures that the message payload is consistent and can be easily parsed by consumers. All messages have a common structure:
    ```json 
        {
            "user_id": 1,
            "date" : "2025-01-16T17:10:26",
            "message": "Account created with ID: 1",
            "data": {"name": "John Doe"}
        }
    ```