import packages

from toolkit.mq.rabbit_mq.core import Consts, Client
from toolkit.mq.rabbit_mq import core

import pika

QUEUE = "hello"

client = Client()
connection = client.connection
channel = client.channel

channel.queue_declare(queue=QUEUE)

