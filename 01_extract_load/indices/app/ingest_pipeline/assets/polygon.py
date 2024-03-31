from ingest_pipeline.connectors.polygon import PolygonApiClient
from ingest_pipeline.connectors.kafka import KafkaClient
import time
import json


async def load_polygon_indicies(
    kafka_client: KafkaClient, messages_buffer: list[str]
) -> None:
    """
    Loads data into a Kafka producer.

    Args:
        kafka_client (KafkaClient): Instance of Kafka client.
        data (list[str]): List of str dict to be loaded into Kafka.
    """
    for messages in messages_buffer:
        messages_list = json.loads(messages)
        for msg in messages_list:
            kafka_client.produce(json.dumps(msg))

    # Flush all messages to Kafka
    kafka_client.flush()


async def extract_load_polygon_indicies(
    polygon_client: PolygonApiClient, kafka_client: KafkaClient, time_threshold: int = 5
) -> None:
    """
    Loads news data into a Kafka producer.

    Args:
        kafka_client (KafkaClient): Instance of Kafka client.
        data (list[dict]): List of news articles to be loaded into Kafka.
    """
    await polygon_client.connect_to_websocket()
    messages_buffer = []  # Buffer to accumulate messages
    last_flush_time = time.time()  # Initialize the last flush time
    while True:
        try:
            # Continuously receive messages
            messages = await polygon_client.receive_messages()
            messages_buffer.append(messages)
            # Check if the time threshold has been reached
            current_time = time.time()
            if current_time - last_flush_time >= time_threshold:
                # Produce messages asynchronously
                await load_polygon_indicies(
                    kafka_client=kafka_client, messages_buffer=messages_buffer
                )
                # Update the last flush time
                last_flush_time = current_time
                messages_buffer.clear()
        except Exception as e:
            print("Error:", e)
            break
