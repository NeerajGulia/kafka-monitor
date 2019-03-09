from panda_db import PandaDB
from api import API
from Debugger import Debugger
import time
import json
from flask import request, abort, jsonify
from flask_restful import Resource, reqparse
import os
from flask import render_template
import logging
import os
from flask_restful import Api
from flask import make_response, Flask
from flask_cors import CORS
import logging
import logging.handlers
import json

application = Flask(__name__)
CORS(application)


DATABASE = "panda"
USER = "postgres"
PASSWORD = "postgres"

pykafka_api = API()
panda_db = PandaDB(DATABASE, USER, PASSWORD)
panda_db.fetch_arrival_rate_for_last_5_min('multiproducer')

log = logging.getLogger(__name__) 

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

class ArrivalRate(Resource):
    def get(self, topic_name):
        cons_lag = pykafka_api.get_consumers_n_lag_by_topic(topic_name)
        print(cons_lag)
        cons_lag['ArrivalRate'] = panda_db.fetch_arrival_rate_for_last_5_min(topic_name)['ArrivalRate']
        return cons_lag

api.add_resource(ArrivalRate, '/api/arrivalrate/<string:topic_name>')

if __name__ == "__main__":
    application.run(host='127.0.0.1', port=9999)