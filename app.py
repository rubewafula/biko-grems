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

app.logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter(
    "%(asctime)s %(levelname)-8s %(name)-5s %(filename)s:%(lineno)d:%(funcName)-10s %(message)s", 
    datefmt="%m-%d-%y %H:%M:%S")

handler = logging.handlers.SysLogHandler(address = '/dev/log')
handler.setFormatter(log_formatter)
app.logger.addHandler(handler)


handler2 = logging.handlers.RotatingFileHandler(filename,
    maxBytes=50*1024*1024, backupCount=5)
handler2.setFormatter(log_formatter)
app.logger.addHandler(handler2)


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
    app.run(host="0.0.0.0",port=9095, debug=True)



