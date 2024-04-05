from ingest_pipeline.connectors.sentiment_api import SentimentApiClient
from ingest_pipeline.connectors.kafka_consumer import KafkaConsumerClient
from ingest_pipeline.connectors.kafka_producer import KafkaProducerClient
import json


def extract_load_transform_news_sentiment(
    sentiment_api_client: SentimentApiClient,
    kafka_consumer_client: KafkaConsumerClient,
    kafka_producer_client: KafkaProducerClient,
) -> None:
    """
    Function to extract news data from Kafka consumer, analyze its sentiment using a sentiment API,
    and load the transformed data into a Kafka producer.

    Args:
        sentiment_api_client (SentimentApiClient): Instance of SentimentApiClient to analyze sentiment.
        kafka_consumer_client (KafkaConsumerClient): Instance of KafkaConsumerClient to consume news data.
        kafka_producer_client (KafkaProducerClient): Instance of KafkaProducerClient to produce transformed data.

    Returns:
        None

    Raises:
        Any exceptions encountered during the process.

    Notes:
        This function continuously consumes messages from the Kafka consumer,
        analyzes the sentiment of news titles using a sentiment API,
        appends sentiment label and score to the message, and produces the transformed message
        to the Kafka producer.

    """
    while True:
        try:
            # Consume a message from Kafka consumer
            msg = kafka_consumer_client.consume()

            # Get sentiment analysis of news title
            sentiment_label, sentiment_score = sentiment_api_client.get_sentiment(
                q=msg.get("title")
            )

            # Append sentiment analysis results to the message
            msg.update(
                {
                    "sentiment_label": sentiment_label,
                    "sentiment_score": sentiment_score,
                }
            )

            # Produce transformed message to Kafka producer
            kafka_producer_client.produce(json.dumps(msg))

        except Exception as e:
            # Handle exceptions gracefully
            print("Error:", e)

            # Close Kafka consumer and flush Kafka producer before exiting
            kafka_consumer_client.close()
            kafka_producer_client.flush()

            # Break the loop
            break
