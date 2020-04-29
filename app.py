from flask import Flask, request
from flask_restful import Api
from time import strftime
from logging.handlers import RotatingFileHandler
import logging
import traceback

from grems_api import (PlaceBetTransaction, AccountBalance, BetOutcomeUpdate, 
    PlaceBetTransactionResponse, AccountBalanceResponse, BetOutcomeUpdateResponse)

app = Flask(__name__)
api = Api(app)

api.add_resource(PlaceBetTransaction,'/api/v1/place-bet-transaction')
api.add_resource(PlaceBetTransactionResponse,'/api/v1/place-bet-transaction/response')

api.add_resource(AccountBalance,'/api/v1/account-balance')
api.add_resource(AccountBalanceResponse,'/api/v1/account-balance/response')

api.add_resource(BetOutcomeUpdate,'/api/v1/bet-outcome-update')
api.add_resource(BetOutcomeUpdateResponse,'/api/v1/bet-outcome-update/response')

filename = '/var/log/grems/grems.api.log'

@app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        app.logger.error('%s %s %s %s %s %s',
                      ts,
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path,
                      response.status)
    return response

@app.errorhandler(Exception)
def exceptions(e):
    """ Logging after every Exception. """
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    app.logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                  ts,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  tb)
    return "Internal Server Error", 500

if __name__ == '__main__':
    # maxBytes to small number, in order to demonstrate the generation of multiple log files (backupCount).
    handler = RotatingFileHandler(filename, maxBytes=10000, backupCount=3)
    # getLogger(__name__):   decorators loggers to file + werkzeug loggers to stdout
    # getLogger('werkzeug'): decorators loggers to file + nothing to stdout
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    app.run(host="0.0.0.0",port=9095, debug=True)



