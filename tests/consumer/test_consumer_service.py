import pytest
import time
import boto3

from unittest.mock import MagicMock

from consumer.service import ConsumerService, SqsMessageBody
from publisher.sns_wrapper import SnsWrapper

@pytest.fixture(scope="module")
def sns_wrapper_fixture():
    sns_wrapper = SnsWrapper(boto3.resource('sns'))

    yield sns_wrapper

@pytest.fixture(scope="module")
def consumer_service_fixture(sns_wrapper_fixture):
    consumer_service = ConsumerService(queue_name="test_queue",listening_time_seconds=5, sns_wrapper=sns_wrapper_fixture)

    yield consumer_service

def test_queue_bindings(consumer_service_fixture):

    # RUN
    consumer_service_fixture.bind_topics(["test_topic_1.fifo","test_topic_2.fifo"])

def test_queue_unbindings(consumer_service_fixture):

    # RUN
    consumer_service_fixture.unbind_topics(["test_topic_1.fifo","test_topic_2.fifo"])

def test_message_consume(consumer_service_fixture):
    # SETUP
    
    # RUN
    test_start = time.perf_counter()
    messages = consumer_service_fixture.__receive_messages__()
    test_duration = time.perf_counter() - test_start

    if len(messages) > 0:
        for message in messages:
            assert message.queue_url
            assert message.body
            assert message.receipt_handle
    if len(messages) == 0:
        assert 5-test_duration>-0.5

def test_messages_listen_nominal_ack(consumer_service_fixture):
    # Setup
    message_counter = 0
    done = False
    def callback(messages):
        nonlocal done
        nonlocal message_counter
        message_counter+=len(messages)
        if message_counter > 20:
            done = True
            raise Exception("Done Testing")

    # Test
    consumer_service_fixture.add_messages_callback(callback)
    consumer_service_fixture.listen()


    assert message_counter > 20
    assert done == True

def test_messages_listen_nominal_nack(consumer_service_fixture):
    # Setup
    message_counter = 0
    done = False
    def callback(messages):
        raise Exception("Check Nack")

    # Test
    consumer_service_fixture.add_messages_callback(callback)
    consumer_service_fixture.listen()

    #TODO: Think what to assert

