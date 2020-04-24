#!/bin/bash
from flask import request,jsonify
from flask_restful import reqparse, abort, Resource
from dicttoxml import dicttoxml
import json
import requests
import re

from flask import current_app as app

global_headers = {
    'Content-Type':'Application/xml',
    'Rcems-Code':'OPRT003',
    'Rcems-Operation':''
}


class PlaceBetTransaction(Resource):


    def post(self):

        args=request.get_json()

        #print(args)

        raw_xml="""<rcems><rcemsMsg><OprtDtl><OprtCode>{operator_code}</OprtCode><ResultUrl>{call_back_url}</ResultUrl></OprtDtl><TrxInfo><OprtTrxId>{transaction_id}</OprtTrxId><MnoTrxId>{mno_ref}</MnoTrxId><MnoName>{mno}</MnoName><BetAmt>{bet_amount}</BetAmt><BetDesc>{bet_desc}</BetDesc><ExpWonAmt>{possible_win}</ExpWonAmt><Ccy>TZS</Ccy><TrxDtTm>{created}</TrxDtTm><PlyrCellNum>{msisdn}</PlyrCellNum><TktNum>{bet_id}</TktNum><Odds>{total_odd}</Odds><ExpBonus>{bonus_amount}</ExpBonus><GameId>{game_id}</GameId><ShopId>{shop_id}</ShopId><Jackpot>{is_jackpot}</Jackpot><OfficeType>{bet_type}</OfficeType><Status>{status}</Status><Rsvd1></Rsvd1> <Rsvd2></Rsvd2><Rsvd3></Rsvd3><Rsvd4></Rsvd4><Rsvd5></Rsvd5></TrxInfo></rcemsMsg><rcemsSgn>672jsdgwer672wt621ghdwqjy2178712te1267638qwwhjsahu6782whkasdbchwetd72eyfshbaute217yiehsafy812urok12pdi012ejdjhy27r62810230-124782hkjkso102839127</rcemsSgn></rcems>"""
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
            operator_code=args.get('operator_code', 'OPRT003')
        )
        print(xml)
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

        raw_xml = """<rcems><rcemsMsg><OprtDtl><OprtCode>{operator_code}</OprtCode><ResultUrl>{call_back_url}</ResultUrl></OprtDtl><TrxInfo><OprtTrxId>{transaction_id}</OprtTrxId><OrgnTktNum>{bet_id}</OrgnTktNum><WonAmt>{possible_win}</WonAmt><Bonus>{bonus_amount}</Bonus><TrxDtTm>{created}</TrxDtTm><Status>{status}</Status><Rsvd1></Rsvd1><Rsvd2></Rsvd2><Rsvd3></Rsvd3><Rsvd4></Rsvd4><Rsvd5></Rsvd5></TrxInfo></rcemsMsg><rcemsSgn>thsihbqwaoewuwekly674298bsdf2t82bneh827324l36j2h56u3952basdq9392612382461741rb2hre51643129128421t3712531263721</rcemsSgn></rcems>"""

        xml = raw_xml.format(
                transaction_id=args.get('transaction_id'),
                bet_id=args.get('bet_id'),
                possible_win=args.get('possible_win'),
                bonus_amount=args.get('bonus_amount'),
                created=args.get('created'),
                status=args.get('status'),
                operator_code=args.get('operator_code'),
                call_back_url=''
        )

        print(xml)
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
        raw_xml = """<rcems><rcemsMsg><OprtDtl><OprtCode>{operator_code}</OprtCode><ResultUrl>{call_back_url}</ResultUrl></OprtDtl><TrxInfo><OprtTrxId>{profile_id}</OprtTrxId><PlyrId>{msisdn}</PlyrId><BlncAmt>{balance}</BlncAmt><Ccy>TZS</Ccy><TrxDtTm>{created}</TrxDtTm><Rsvd1></Rsvd1<Rsvd2></Rsvd2><Rsvd3></Rsvd3><Rsvd4></Rsvd4><Rsvd5></Rsvd5></TrxInfo></rcemsMsg><rcemsSgn>hsjdksbwt32764323hsgatdq76e23gd762egydg727r823grbjnj27r238r926128cnc2e7b1nr92r328b68527cypqxq6rqbxn</rcemsSgn></rcems>"""

        xml = raw_xml.format(
            profile_id=args.get('profile_id'),
            msisdn=args.get('msisdn'),
            balance=args.get('balance'),
            created=args.get('created'),
            operator_code=args.get('operator_code'),
            call_back_url=''
        )

        print(xml)
        global_headers['Rcems-Operation'] = 'pabtrxn'
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
        xml =  request.data
        transaction_id = re.search('<OprtTrxId\>(.*)<\/OprtTrxId>', xml, re.IGNORECASE).group(1)
        status_code = re.search('<TrxStsCode\>(.*)<\/TrxStsCode>', xml, re.IGNORECASE).group(1)

        #TODO: Push this to Queue

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
        xml =  request.data
        transaction_id = re.search('<OprtTrxId\>(.*)<\/OprtTrxId>', xml, re.IGNORECASE).group(1)
        status_code = re.search('<TrxStsCode\>(.*)<\/TrxStsCode>', xml, re.IGNORECASE).group(1)

        # TODO: Push this to Queue

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
        xml =  request.data
        transaction_id = re.search('<OprtTrxId\>(.*)<\/OprtTrxId>', xml, re.IGNORECASE).group(1)
        status_code = re.search('<TrxStsCode\>(.*)<\/TrxStsCode>', xml, re.IGNORECASE).group(1)

        # TODO: Push this to Queue

        app.logger.info("AccountBalanceResponse Transaction code [%s], status code [%s]" % (
            transaction_id, status_code)
        )

        return "<rcemsTrxSubReqAck>TrxStsCode>GBT0000</TrxStsCode></rcemsTrxSubReqAck>"


class DailyBalanceList(Resource):



    def get(self,trans_id):
        pass

    def post(self):
        args=request.get_json()
        trans_id = int(max(dailyTransaction.keys())) + 1
        dailyTransaction[trans_id]=args
        xml = dicttoxml(dailyTransaction,attr_type=False, custom_root="TrxInfo")
        response= requests.post('http://196.192.79.29/api/transactions/qrequest', data=xml, headers=headers).text
        print(xml)
        return dailyTransaction










