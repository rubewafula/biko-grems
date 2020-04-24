from amqplib import client_0_8 as amqp
from flask import current_app as app
import configparser
import os
import json


class Publisher(object):

    GREMS_BET_RESPONSE_QUEUE = 'GREMS_BET_RESPONSE_QUEUE'
    GREMS_BET_UPDATE_QUEUE = 'GREMS_BET_UPDATE_RESPONSE_QUEUE'
    GREMS_PROFILE_BALANCE_QUEUE = 'GREMS_PROFILE_BALANCE_RESPONSE_QUEUE'

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
            conn = amqp.Connection(host=self.configs['rabbithost'],
                userid=self.configs['rabbitusername'],
                password=self.configs['rabbitpassword'],
                virtual_host=self.configs['rabbitvhost'] or "/",
                insist=False)
        except Exception as e:
            app.logger.error("Error attempting to get Rabbit Connection: %r " % e)
            return;

        app.logger.info("Connection to rabbit established to Q... [%s]" % queue)
        queue = self.get_queue_name(msg_type)
        exchange = self.get_exchange(queue)
        routing_key = self.get_routing_key(queue)
        try:
            ch = conn.channel()
            msg = amqp.Message(json.dumps(message))
            msg.properties["content_type"] = "text/plain"
            msg.properties["delivery_mode"] = 2
            ch.basic_publish(exchange=exchange,
                             routing_key=routing_key,
                             msg=msg)
            app.logger.info("Message published OK ... ")
        except Exception as e:
            app.logger.error("Error attempting to publish to Rabbit: Bonus %r " % e)
            conn.close()
        else:
            ch.close()
            conn.close()

