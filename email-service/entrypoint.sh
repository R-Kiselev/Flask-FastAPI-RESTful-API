#!/bin/bash

uvicorn app.main:app --ssl-keyfile key.pem --ssl-certfile cert.pem --host 0.0.0.0 --port 8001