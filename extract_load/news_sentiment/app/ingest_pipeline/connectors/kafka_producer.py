from confluent_kafka import Producer


class KafkaProducerClient:
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
        Initializes a Kafka producer client instance.

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
                "bootstrap.servers": self.bootstrap_servers,
                "security.protocol": self.security_protocol,
                "sasl.mechanisms": self.sasl_mechanisms,
                "sasl.username": self.sasl_username,
                "sasl.password": self.sasl_password,
            }
        )

    def produce(self, data: list):
        """
        Produces messages to the configured Kafka topic.

        Args:
            data (list): List of dictionaries representing messages to be produced.
        """
        if data:
            # Produce each message to the Kafka topic
            self.producer.produce(
                self.topic_name,
                key=None,
                value=data,
            )
        # Poll Kafka for messages (0 indicates non-blocking operation)
        self.producer.poll(0)

    def flush(self):
        """
        Flushes the Kafka producer to ensure all messages are sent.
        """
        self.producer.flush()
