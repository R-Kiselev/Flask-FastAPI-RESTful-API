from fastapi import FastAPI, Request

from .rabbitmq.run_manager import MessageQueueRunner


def create_app() -> FastAPI:
    app = FastAPI()

    configure_services(app)
    configure_event_handlers(app)

    return app


def configure_services(app: FastAPI) -> None:
    # app.state is a special attribute that allows you to store arbitrary data
    app.state.message_queue_runner = MessageQueueRunner()


def configure_event_handlers(app: FastAPI) -> None:
    app.add_event_handler(
        "startup", app.state.message_queue_runner.start_messages_listener)
    app.add_event_handler(
        "shutdown", app.state.message_queue_runner.stop_message_listener)


app = create_app()