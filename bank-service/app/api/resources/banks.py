from datetime import datetime
import requests 

from flask import request
from flask_jwt_extended import jwt_required, get_jwt

from app.commons.base_resources import BaseObjectResource, BaseListResource
from app.models.bank import Bank
from app.api.schemas.bank import BankSchema
from app.auth.utils import user_roles_required

from app.extensions import message_queue_client
from app.api.schemas.message import MessageSchema
from app.config import LOG_SERVICE_URL


class BankObjectRes(BaseObjectResource):
    model = Bank
    schema = BankSchema()

    method_decorators = {
        'get': [user_roles_required('admin', 'manager', 'user'), jwt_required()],
        'put': [user_roles_required('admin', 'manager'), jwt_required()],
        'delete': [user_roles_required('admin', 'manager'), jwt_required()]
    }


class BankListRes(BaseListResource):
    model = Bank
    schema = BankSchema()

    method_decorators = {
        'get': [user_roles_required('admin', 'manager', 'user'), jwt_required()],
        'post': [user_roles_required('admin', 'manager'), jwt_required()]
    }

    def post(self):
        response, status_code = super().post()
        jwt = get_jwt()

        message = {
            'user_id': jwt.get('user_id'),
            'date': datetime.now(),
            'message': f'Bank created with ID: {response.get('item').get('id')}',
            'data': request.json
        }
        message_data = MessageSchema().dump(message)
        reply = message_queue_client.send_message(
            message_data, 'bank.created', need_reply=True)

        if reply:
            # Send HTTP POST request to log-service /logs endpoint to save the message
            try:
                print('Sending HTTP request')
                res = requests.post(
                    url=LOG_SERVICE_URL + "/logs",
                    json=message_data,
                    timeout=1
                )
                print(f"Got response from log-service: {res.json()}")
            except Exception as e:
                print(f"Can't save message in log-service, error : {e}")

        return response, status_code
