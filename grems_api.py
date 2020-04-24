#!/bin/bash
from flask import request,jsonify
from flask_restful import reqparse, abort, Resource
from publisher import Publisher
import configparser
import json
import requests
import re
import os

from flask import current_app as app

global_headers = {
    'Content-Type':'Application/xml',
    'Rcems-Code':'OPRT003',
    'Rcems-Operation':''
}

class Config(object):
    @staticmethod
    def read(section=None):
        try:
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.join(cur_dir, 'config/configs.ini')
            cparser = configparser.ConfigParser()
            cparser.read(filename)
            config_dic = {}
            section = section or 'BIKO'
            options = cparser.options(section)
            for option in options:
                try:
                    config_dic[option] = cparser.get(section, option)
                    if config_dic[option] == -1:
                        pass
                except:
                    config_dic[option] = None
            return config_dic
        except Exception as e:
            return {} 


class PlaceBetTransaction(Resource):


    def post(self):

        args=request.get_json()

        conf = Config.read('BIKO')

        raw_xml="""<rcems><rcemsMsg><OprtDtl><OprtCode>{operator_code}</OprtCode><ResultUrl>{call_back_url}</ResultUrl></OprtDtl><TrxInfo><OprtTrxId>{transaction_id}</OprtTrxId><MnoTrxId>{mno_ref}</MnoTrxId><MnoName>{mno}</MnoName><BetAmt>{bet_amount}</BetAmt><BetDesc>{bet_desc}</BetDesc><ExpWonAmt>{possible_win}</ExpWonAmt><Ccy>TZS</Ccy><TrxDtTm>{created}</TrxDtTm><PlyrCellNum>{msisdn}</PlyrCellNum><TktNum>{bet_id}</TktNum><Odds>{total_odd}</Odds><ExpBonus>{bonus_amount}</ExpBonus><GameId>{game_id}</GameId><ShopId>{shop_id}</ShopId><Jackpot>{is_jackpot}</Jackpot><OfficeType>{bet_type}</OfficeType><Status>{status}</Status><Rsvd1></Rsvd1> <Rsvd2></Rsvd2><Rsvd3></Rsvd3><Rsvd4></Rsvd4><Rsvd5></Rsvd5></TrxInfo></rcemsMsg><rcemsSgn>{enc_sign}</rcemsSgn></rcems>"""
        xml=raw_xml.format(
            transaction_id = args.get('transaction_id'),
            mno_ref=args.get('mno_ref'),
            mno=args.get('mno'),
            bet_amount=args.get('bet_amount'),
            bet_desc=args.get('bet_desc'),
            possible_win=args.get('possible_win'),
            created=args.get('created'),
            msisdn=args.get('msisdn'),
            bet_id=args.get('bet_id'),
            total_odd=args.get('total_odd'),
            bonus_amount=args.get('bonus_amount'),
            game_id=args.get('game_id'),
            shop_id=args.get('shop_id'),
            is_jackpot=args.get('is_jackpot'),
            bet_type=args.get('office_type', 'Online'),
            status=args.get('status', 'BET'),
            call_back_url='',
            operator_code=args.get('operator_code', 'OPRT003'),
            enc_sign=conf.get('encryption_key')
        )
        #print(xml)
        global_headers['Rcems-Operation'] = 'sbtrxn'
        response= requests.post('http://196.192.79.29/api/transactions/qrequest', data=xml, headers=global_headers).text
        #print(xml)
        response_code = re.search('<TrxStsCode\>(.*)<\/TrxStsCode>', response, re.IGNORECASE).group(1)
        app.logger.info("PlaceBetTransaction Created [%s], MSISDN [%s] "\
                "BetID [%s], Bet Amount [%s], Bonus Amount [%s] | RESPONSE [%s] "\
                % (
                    args.get('created'), args.get('msisdn'), args.get('bet_id'), 
                    args.get('bet_amount'), args.get('bonus_amount'), response_code 
                )
        )

        return response

class BetOutcomeUpdate(Resource):
    def get(self):
        pass

    def post(self):
        args=request.get_json()
        
        conf = Config.read('BIKO')

        raw_xml = """<rcems><rcemsMsg><OprtDtl><OprtCode>{operator_code}</OprtCode><ResultUrl>{call_back_url}</ResultUrl></OprtDtl><TrxInfo><OprtTrxId>{transaction_id}</OprtTrxId><OrgnTktNum>{bet_id}</OrgnTktNum><WonAmt>{possible_win}</WonAmt><Bonus>{bonus_amount}</Bonus><TrxDtTm>{created}</TrxDtTm><Status>{status}</Status><Rsvd1></Rsvd1><Rsvd2></Rsvd2><Rsvd3></Rsvd3><Rsvd4></Rsvd4><Rsvd5></Rsvd5></TrxInfo></rcemsMsg><rcemsSgn>{enc_sign}</rcemsSgn></rcems>"""

        xml = raw_xml.format(
                transaction_id=args.get('transaction_id'),
                bet_id=args.get('bet_id'),
                possible_win=args.get('possible_win'),
                bonus_amount=args.get('bonus_amount'),
                created=args.get('created'),
                status=args.get('status'),
                operator_code=args.get('operator_code'),
                call_back_url='',
                enc_sign=conf.get('encryption_key')
        )

        #print(xml)
        global_headers['Rcems-Operation'] = 'sbutrxn'
        response= requests.post('http://196.192.79.29/api/transactions/qrequest', data=xml, headers=global_headers).text
        response_code = re.search('<TrxStsCode\>(.*)<\/TrxStsCode>', response, re.IGNORECASE).group(1)
        
        app.logger.info("BetOutcomeUpdate Created [%s], "\
                "BetID [%s], Possible WIN [%s], Bonus Amount [%s] | RESPONSE [%s] "\
                % (
                    args.get('created'), args.get('bet_id'),
                    args.get('possible_win'), args.get('bonus_amount'), response_code
                )
        )

        return response

class AccountBalance(Resource):
    def get(self):
        pass

    def post(self):
        args=request.get_json()
        
        conf = Config.read('BIKO')

        raw_xml = """<rcems><rcemsMsg><OprtDtl><OprtCode>{operator_code}</OprtCode><ResultUrl>{call_back_url}</ResultUrl></OprtDtl><TrxInfo><OprtTrxId>{profile_id}</OprtTrxId><PlyrId>{msisdn}</PlyrId><BlncAmt>{balance}</BlncAmt><Ccy>TZS</Ccy><TrxDtTm>{created}</TrxDtTm><Rsvd1></Rsvd1><Rsvd2></Rsvd2><Rsvd3></Rsvd3><Rsvd4></Rsvd4><Rsvd5></Rsvd5></TrxInfo></rcemsMsg><rcemsSgn>{enc_sign}</rcemsSgn></rcems>"""

        xml = raw_xml.format(
            profile_id=args.get('profile_id'),
            msisdn=args.get('msisdn'),
            balance=args.get('balance'),
            created=args.get('created'),
            operator_code=args.get('operator_code'),
            call_back_url='',
            enc_sign=conf.get('encryption_key')
        )

        #print(xml)
        global_headers['Rcems-Operation'] = 'pabtrxn'
        #print(global_headers)

        response= requests.post('http://196.192.79.29/api/transactions/qrequest', data=xml, headers=global_headers).text
        response_code = re.search('<TrxStsCode\>(.*)<\/TrxStsCode>', response, re.IGNORECASE).group(1)

        app.logger.info("AccountBalance  Created [%s], "\
                "Profile [%s], MSISDN [%s], BALANCE [%s] | RESPONSE [%s] "\
                % (
                    args.get('created'), args.get('profile_id'),
                    args.get('msisdn'), args.get('balance'), response_code
                )
        )

        return response



class PlaceBetTransactionResponse(Resource):

    """             
    <rcemsTrxSubResp>
        <OprtTrxId>ID91003</OprtTrxId>
        <TrxStsCode>GBT0000</ TrxStsCode>
    </rcemsTrxSubResp>
    """
    def post(self):
        xml =  request.stream.read().decode('utf-8')
        transaction_id = re.search('<OprtTrxId\>(.*)<\/OprtTrxId>', xml, re.IGNORECASE).group(1)
        status_code = re.search('<TrxStsCode\>(.*)<\/TrxStsCode>', xml, re.IGNORECASE).group(1)
        message = {'transaction_id':transaction_id, 'status_code':status_code}

        # Push this to Queue
        conf = Config.read('RABBIT')
        publisher = Publisher(conf)
        publisher.publish_message(message)

        app.logger.info("PlaceBetTransactionResponse Transaction code [%s], status code [%s]" % (
            transaction_id, status_code)
        )

        return "<rcemsTrxSubReqAck>TrxStsCode>GBT0000</TrxStsCode></rcemsTrxSubReqAck>"


class BetOutcomeUpdateResponse(Resource):

    """
    <rcemsTrxSubResp>
        <OprtTrxId>ID91003</OprtTrxId>
        <TrxStsCode>GBT0000</ TrxStsCode>
    </rcemsTrxSubResp>
    """
    def post(self):
        xml =  request.stream.read().decode('utf-8')
        transaction_id = re.search('<OprtTrxId\>(.*)<\/OprtTrxId>', xml, re.IGNORECASE).group(1)
        status_code = re.search('<TrxStsCode\>(.*)<\/TrxStsCode>', xml, re.IGNORECASE).group(1)
        message = {'transaction_id':transaction_id, 'status_code':status_code}

        # Push this to Queue
        conf = Config.read('RABBIT')
        publisher = Publisher(conf)
        publisher.publish_message(message, 'BETUPDATE')        
        
        app.logger.info("PlaceBetTransactionResponse Transaction code [%s], status code [%s]" % (
            transaction_id, status_code)
        )

        return "<rcemsTrxSubReqAck>TrxStsCode>GBT0000</TrxStsCode></rcemsTrxSubReqAck>"


class AccountBalanceResponse(Resource):

    """
    <rcemsTrxSubResp>
        <OprtTrxId>ID91003</OprtTrxId>
        <TrxStsCode>GBT0000</ TrxStsCode>
    </rcemsTrxSubResp>
    """
    def post(self):
        xml =  request.stream.read().decode('utf-8')
        transaction_id = re.search('<OprtTrxId\>(.*)<\/OprtTrxId>', xml, re.IGNORECASE).group(1)
        status_code = re.search('<TrxStsCode\>(.*)<\/TrxStsCode>', xml, re.IGNORECASE).group(1)

        message = {'transaction_id':transaction_id, 'status_code':status_code}

        # Push this to Queue
        conf = Config.read('RABBIT')
        publisher = Publisher(conf)
        publisher.publish_message(message, 'ACC')
        
        app.logger.info("AccountBalanceResponse Transaction code [%s], status code [%s]" % (
            transaction_id, status_code)
        )

        return "<rcemsTrxSubReqAck>TrxStsCode>GBT0000</TrxStsCode></rcemsTrxSubReqAck>"

