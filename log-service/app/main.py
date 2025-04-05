from fastapi import FastAPI

from .db import connect_and_init_db, close_db_connection
from .resources.logs import router as logs_router
from .rabbitmq.run_manager import MessageQueueRunner


def create_app() -> FastAPI:
    app = FastAPI()

    configure_services(app)
    configure_event_handlers(app)
    add_routers(app)

    return app


def configure_services(app: FastAPI) -> None:
    # app.state is a special attribute that allows you to store arbitrary data
    app.state.message_queue_runner = MessageQueueRunner()


def configure_event_handlers(app: FastAPI) -> None:
    app.add_event_handler("startup", connect_and_init_db)
    app.add_event_handler("shutdown", close_db_connection)
    app.add_event_handler(
        "startup", app.state.message_queue_runner.start_messages_listener)
    app.add_event_handler(
        "shutdown", app.state.message_queue_runner.stop_message_listener)


def add_routers(app: FastAPI) -> None:
    app.include_router(logs_router)


app = create_app()