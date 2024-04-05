from confluent_kafka import Consumer, KafkaError, KafkaException
import sys
import json


class KafkaConsumerClient:
    def __init__(
        self,
        bootstrap_servers: str,
        security_protocol: str,
        sasl_mechanisms: str,
        sasl_username: str,
        sasl_password: str,
        topic_name: str,
    ):
        """
        Initializes a Kafka consumer client instance.

        Args:
            bootstrap_servers (str): Comma-separated list of broker addresses.
            security_protocol (str): Security protocol used for communication.
            sasl_mechanisms (str): SASL mechanisms for authentication.
            sasl_username (str): Username for SASL authentication.
            sasl_password (str): Password for SASL authentication.
            topic_name (str): Name of the Kafka topic.
        """
        self.bootstrap_servers = bootstrap_servers
        self.security_protocol = security_protocol
        self.sasl_mechanisms = sasl_mechanisms
        self.sasl_username = sasl_username
        self.sasl_password = sasl_password
        self.topic_name = topic_name

        # Configure and subscribe to Kafka topic
        self.consumer = Consumer(
            {
                "bootstrap.servers": self.bootstrap_servers,
                "security.protocol": self.security_protocol,
                "sasl.mechanisms": self.sasl_mechanisms,
                "sasl.username": self.sasl_username,
                "sasl.password": self.sasl_password,
                "group.id": "consumer_group",  # Modify accordingly
                "auto.offset.reset": "earliest",
            }
        )
        self.consumer.subscribe([self.topic_name])

    def consume(self) -> dict:
        """
        Consume messages from the subscribed Kafka topic.

        Returns:
            dict: The consumed message.
        Raises:
            KafkaException: If an error occurs during consumption.
        """
        while True:
            try:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition
                        print(
                            "%% %s [%d] reached end at offset %d\n"
                            % (msg.topic(), msg.partition(), msg.offset())
                        )
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    # Return consumed message
                    return json.loads(msg.value())

            except KeyboardInterrupt:
                # Interrupted by user
                sys.stderr.write("%% Aborted by user\n")
                self.consumer.close()

    def close(self):
        """
        Closes the Kafka consumer.
        """
        self.consumer.close()
