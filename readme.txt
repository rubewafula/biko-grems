#!/bin/bash

Author Reuben Paul Wafula
This is not a small interface to push transactions to GREMS.
(Tanzania Betting Board API interface in accordance to regulations for the Board)

Build on stupid RAW XML over requests python API
And yes uses stupid regex parser when the XML is small enough

Checkout below main API test


BELOW ARE TESTS OVER GREMS FOR BIKO
-----------------------------------------------------------------------------------------------
1.  curl -XPOST  -d '{"transaction_id":123,"mno_ref":8292,"mno":"TIGO","bet_amount":500,"bet_desc":"Manchester United","possible_win":1220, "created":"2020-04-24T16:09:00","msisdn":255726986944,"bet_id":6377363,"total_odd":2, "bonus_amount":220,"game_id":4546,"shop_id":"NA", "is_jackpot":"false","office_type":"Online","status":"BET","call_back_url":"","operator_code":"OPRT003"}' -H "content-type:application/json" 'http://127.0.0.1:8000/api/v1/place-bet-transaction'


"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><rcemsTrxSubReqAck><TrxStsCode>GBT0000</TrxStsCode></rcemsTrxSubReqAck>"



2. curl -XPOST  -d '{"transaction_id":123,"possible_win":1220, "created":"2020-04-18T21:01:00","bet_id":6377363, "bonus_amount":220, "status":"WON","call_back_url":"","operator_code":"OPRT003"}' -H "content-type:application/json" 'http://127.0.0.1:8000/api/v1/bet-outcome-update'

"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><rcemsTrxSubReqAck><TrxStsCode>GBT0000</TrxStsCode></rcemsTrxSubReqAck>"



3. curl -XPOST  -d '{"profile_id":123,"msisdn":255726986944, "created":"2020-04-18 21:01,323","balance":6377, "call_back_url":"","operator_code":""}' -H "content-type:application/json" 'http://127.0.0.1:8000/api/v1/account-balance

RESPONSE
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><rcemsTrxSubReqAck><TrxStsCode>GBT0002</TrxStsCode></rcemsTrxSubReqAck>"


FTP push os transactions every day


Work to be dome by cron ..

1. Push bets to Q
2. Push active balances to Q
3. Push FTP trnsactions to Q



Work to be Done bu InboxConsume
Push from Q to GREMS API

HOW TO INSTALL
--------------------------------------------------------------------------------------------------

1. You need to run this in server container, I have done httpd for now
(Make sure wsgi module for httpd is installed)

2. Make httpd to listen to port 9095 (This can be changed in the httpd.conf file included in project root dir)
3. Clone project to /var/www/html/grems-biko or directory of your choice
4. Create python virtual-env in root folder (named v) - done on python3.6 
   Note: if the folder is not named as above remeber to update paths in grems.wsgi file
5. Copy file httpd.conf to server conf dir /etc/httpd/conf you can rename it appropriately
6. Make sure path defined in httpd.conf relate to the location of the project - this project is assumed to be installed in /var/www/html/grems-biko
7. Ensure log dir is created and writable by httpd /var/log/grems
8. check config/configs.ini and apply appropriate encryption_key and rabbit connections params

8. Restart httpd

Just in case u need to dial a help, rubewafula@gmail.com can accept a mail on this
