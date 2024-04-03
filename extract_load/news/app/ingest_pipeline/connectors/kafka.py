from confluent_kafka import Producer
import json
import sys


class KafkaClient:
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
        Initializes a Kafka client instance.

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

        # Initialize Kafka producer
        self.producer = Producer(
            {
                "bootstrap.servers": bootstrap_servers,
                "security.protocol": security_protocol,
                "sasl.mechanisms": sasl_mechanisms,
                "sasl.username": sasl_username,
                "sasl.password": sasl_password,
            }
        )

    def produce(self, data: list):
        """
        Produces messages to the Kafka topic.

        Args:
            data (list): List of dictionaries representing messages to be produced.
        """

        def delivery_callback(err, msg):
            """
            Delivery callback function.

            Args:
                err: Error message if delivery fails.
                msg: Message object containing delivery information.
            """
            pass
            # if err:
            #     sys.stderr.write("Error: Message delivery failed: %s\n" % err)
            # else:
            #     sys.stderr.write(
            #         "Message delivered to %s [%d] @ %d\n"
            #         % (msg.topic(), msg.partition(), msg.offset())
            #     )

        if data:
            # Produce each message to the Kafka topic
            for piece in data:
                json_piece = json.dumps(piece)
                self.producer.produce(
                    self.topic_name,
                    key=None,
                    value=json_piece.encode("utf-8"),
                    callback=delivery_callback,
                )
        # Poll Kafka for messages (0 indicates non-blocking operation)
        self.producer.poll(0)

    def flush(self):
        self.producer.flush()
