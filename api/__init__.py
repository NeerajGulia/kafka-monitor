import os
from flask_restful import Api
from flask import make_response, Flask
from flask_cors import CORS
import logging
import logging.handlers
import json

application = Flask(__name__)
CORS(application)

def output_json(obj, code, headers=None):
    resp = make_response(json.dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

api = Api(application)
api.representations = {'application/json': output_json}

# Logging section
logLevel = os.environ.get('LOG_LEVEL')
if not logLevel:
    logLevel = logging.ERROR

handler = logging.FileHandler(os.environ.get("LOGFILE", "panda.log"))
formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logLevel)
logger.addHandler(handler)

kafka_brokers = ['13.234.16.29:9092', '13.127.51.155:9092', '13.232.11.220:9092']

import api.rest