from contextlib import contextmanager
import logging
import socket
from time import sleep

from django.conf import settings
import pika
from pydantic import BaseModel
from retry import retry

from .callback_decorator import Callback as CallbackBase

logger = logging.getLogger('messaging')


class Callback(CallbackBase):
    @staticmethod
    def reject_message(channel, method_frame, header_frame, body):
        channel.basic_reject(method_frame.delivery_tag)

    @staticmethod
    def resend_message_later(channel, method_frame, header_frame, body):
        sleep(3)

    @staticmethod
    def acknowledge_message(channel, method_frame, header_frame, body):
        channel.basic_ack(method_frame.delivery_tag)


@retry(
    (
        pika.exceptions.AMQPConnectionError,
        pika.exceptions.ConnectionClosedByBroker,
        socket.gaierror,
    ),
    delay=5
)
def start_consumer(routing_key: str, do_callback: callable):
    logger.info('Starting consumer; routing_key=%s', routing_key)

    with create_channel_prepared_for_consuming(routing_key) as channel:
        channel.basic_consume(queue=routing_key, on_message_callback=do_callback, auto_ack=False)

        try:
            channel.start_consuming()

        finally:
            channel.stop_consuming()


@contextmanager
def create_channel():
    with \
            pika.BlockingConnection(pika.URLParameters(settings.FMS_RMQ_URL)) as connection, \
            connection.channel() as channel:
        yield channel


@contextmanager
def create_channel_prepared_for_consuming(routing_key: str):
    with create_channel() as channel:

        channel.basic_qos(prefetch_count=1)  # Only fetch one message at once.

        _declare_exchange(channel)

        channel.queue_declare(queue=routing_key, exclusive=False, durable=True, auto_delete=False)

        channel.queue_bind(exchange=settings.FMS_RMQ_EXCHANGE, queue=routing_key, routing_key=routing_key)

        yield channel


def _declare_exchange(channel):
    channel.exchange_declare(exchange=settings.FMS_RMQ_EXCHANGE, exchange_type=pika.exchange_type.ExchangeType.direct)

    logger.info('Exchange declared; exchange=%s', settings.FMS_RMQ_EXCHANGE)


def send_message(routing_key: str, message: BaseModel):
    logger.info('Sending message; message=%s, routing_key=%s', message, routing_key)
    with create_channel() as channel:

        _declare_exchange(channel)

        channel.basic_publish(
            exchange=settings.FMS_RMQ_EXCHANGE,
            routing_key=routing_key,
            body=message.json().encode(),
        )
