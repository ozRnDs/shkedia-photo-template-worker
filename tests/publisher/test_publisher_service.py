from pydantic import BaseModel
import logging
logger = logging.getLogger(__name__)
import pytest
from uuid import uuid4

from publisher.service import PublisherService

@pytest.fixture(scope="module")
def publisher_service_fixture():
    publisher_service = PublisherService(topic_names=["test_topic_1.fifo","test_topic_2.fifo"])

    yield publisher_service


def test_publish_text_message(publisher_service_fixture):
    # Setup

    class TestMessageClass(BaseModel):
        media_id: str
        name: str
    # RUN
    for i in range(100):
        message = TestMessageClass(media_id=str(uuid4()), name=f"MediaNumber{i}")
        topic_index = i % 2
        topic_id = (list)(publisher_service_fixture.topics.keys())[topic_index]
        value = publisher_service_fixture.publish(topic_id, message, message.media_id)
        logger.info(value)
