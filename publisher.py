from flask import current_app as app
import configparser
import os
import json
import pika

class Publisher(object):

    GREMS_BET_RESPONSE_QUEUE = 'GREMS_BET_TRANSACTION_RESPONSE_QUEUE'
    GREMS_BET_UPDATE_QUEUE = 'GREMS_BET_UPDATE_RESPONSE_QUEUE'
    GREMS_PROFILE_BALANCE_QUEUE = 'GREMS_ACCOUNT_UPDATE_RESPONSE_EXCHANGE'

    def __init__(self, configs):
        self.configs = configs

   
    def get_queue_name(self, qtype):
        if qtype=='BET':
            return self.GREMS_BET_RESPONSE_QUEUE
        elif qtype=='BETUPDATE':
            return self.GREMS_BET_UPDATE_QUEUE
        elif qtype == 'ACC':
            return self.GREMS_PROFILE_BALANCE_RESPONSE_QUEUE
        # Default to this    
        return self.GREMS_BET_RESPONSE_QUEUE

    def get_routing_key(self, queue):
        return queue.replace('QUEUE', 'ROUTE')

    def get_exchange(self, queue):
        return queue.replace('QUEUE', 'EXCHANGE')

    def publish_message(self, message, msg_type='BET'):
        app.logger.info("FOUND MESSAGE Bonus posting to Q: [%s] Message %r " % (msg_type,message))
        try:
            credentials = pika.PlainCredentials(self.configs['rabbitusername'], self.configs['rabbitpassword'])
            parameters = pika.ConnectionParameters(self.configs['rabbithost'],
                                       5672,
                                       self.configs['rabbitvhost'] or "/",
                                       credentials)

            conn =  pika.BlockingConnection(parameters)

        except Exception as e:
            app.logger.error("Error attempting to get Rabbit Connection: %r " % e)
            return;

        app.logger.info("Connection established, preparing to publish message TYPE [%s],MESSAGE [%s]" % (msg_type, message))
        queue = self.get_queue_name(msg_type)
        exchange = self.get_exchange(queue)
        routing_key = self.get_routing_key(queue)
        try:
            ch = conn.channel()
            headers = {"content-type":"text/plain"}
            ch.basic_publish(
		        exchange=exchange,
		        routing_key=routing_key,
		        body=json.dumps(message), # must be string
		        properties=pika.BasicProperties(
			        delivery_mode=2, # makes persistent job
			        priority=0, # default priority
			        headers=headers
		        )
            )

            app.logger.info("Message published OK ... to EXC [%s]" % exchange)
        except Exception as e:
            app.logger.error("Error attempting to publish to Rabbit: Bonus %r " % e)
            conn.close()
        else:
            ch.close()
            conn.close()

