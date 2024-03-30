import asyncio
import json
import websockets
import os
from dotenv import load_dotenv
from confluent_kafka import Producer
import sys
import time


def delivery_callback(err, msg):
    if err:
        sys.stderr.write("Error: Message delivery failed: %s\n" % err)
    else:
        sys.stderr.write(
            "Message delivered to %s [%d] @ %d\n"
            % (msg.topic(), msg.partition(), msg.offset())
        )


async def produce_messages(producer, topic_name, messages_buffer):
    # Produce all messages in the buffer
    for messages in messages_buffer:
        messages_list = json.loads(messages)
        for msg in messages_list:
            producer.produce(topic_name, json.dumps(msg), callback=delivery_callback)

    # Flush all messages to Kafka
    producer.flush()


async def consume_minute_aggregates():
    load_dotenv()
    uri = "wss://delayed.polygon.io/indices"
    api_key = os.environ.get("POLYGON_API_KEY")

    # Kafka producer configuration
    producer = Producer(
        {
            "bootstrap.servers": os.environ.get("bootstrap.servers"),
            "security.protocol": os.environ.get("security.protocol"),
            "sasl.mechanisms": os.environ.get("sasl.mechanisms"),
            "sasl.username": os.environ.get("sasl.username"),
            "sasl.password": os.environ.get("sasl.password"),
        }
    )
    topic_name = os.environ.get("kafka_topic_name")

    async with websockets.connect(uri) as websocket:
        # Authentication message
        auth_message = {"action": "auth", "params": api_key}
        await websocket.send(json.dumps(auth_message))

        # Subscription message for real-time minute aggregates
        subscription_message = {"action": "subscribe", "params": "AM.*"}
        await websocket.send(json.dumps(subscription_message))

        # Define the time threshold (in seconds)
        TIME_THRESHOLD = 5

        messages_buffer = []  # Buffer to accumulate messages
        last_flush_time = time.time()  # Initialize the last flush time

        # Continuously receive and process messages
        while True:
            try:
                messages = await websocket.recv()
                print("Received message:", messages)
                messages_buffer.append(messages)
                # Check if the time threshold has been reached
                current_time = time.time()
                if current_time - last_flush_time >= TIME_THRESHOLD:
                    # Produce messages asynchronously
                    await produce_messages(producer, topic_name, messages_buffer)
                    # Update the last flush time
                    last_flush_time = current_time
                    messages_buffer.clear()

            except websockets.exceptions.ConnectionClosedError:
                print("Connection to WebSocket closed unexpectedly")
                break
            except Exception as e:
                print("Error:", e)
                break


async def main():
    await consume_minute_aggregates()


if __name__ == "__main__":
    asyncio.run(main())
