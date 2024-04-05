from dotenv import load_dotenv
import os
from pathlib import Path
from ingest_pipeline.connectors.sentiment_api import SentimentApiClient
from ingest_pipeline.connectors.kafka_consumer import KafkaConsumerClient
from ingest_pipeline.connectors.kafka_producer import KafkaProducerClient
from ingest_pipeline.assets.pipeline_logging import PipelineLogging
from ingest_pipeline.assets.sentiment import extract_load_transform_news_sentiment
import yaml
import time


def pipeline(pipeline_logging: PipelineLogging):
    """
    Main pipeline function that orchestrates data extraction and loading.

    Args:
        pipeline_logging (PipelineLogging): Instance of PipelineLogging for logging.

    Raises:
        Exception: If any error occurs during the pipeline execution.
    """
    try:
        pipeline_logging.logger.info("Starting pipeline run")

        # Load environment variables
        pipeline_logging.logger.info("Loading pipeline environment variables")
        load_dotenv()

        # Extract configuration settings from environment variables
        SENTIMENT_API_HOST = os.environ.get("sentiment_api_host")
        KAFKA_HOST = os.environ.get("bootstrap_servers")
        KAFKA_PROTOCOL = os.environ.get("security_protocol")
        KAFKA_SASL_MECHANISMS = os.environ.get("sasl_mechanisms")
        KAFKA_USERNAME = os.environ.get("sasl_username")
        KAFKA_PASSWORD = os.environ.get("sasl_password")
        SOURCE_TOPIC_NAME = "polygon_news_topic"
        TARGET_TOPIC_NAME = "polygon_news_sentiment_topic"

        # Create SentimentApiClient instance
        pipeline_logging.logger.info("Creating Sentiment API client")
        sentiment_api_client = SentimentApiClient(url=SENTIMENT_API_HOST)

        # Connect to Kafka consumer
        pipeline_logging.logger.info("Connecting to Kafka consumer")
        kafka_consumer_client = KafkaConsumerClient(
            bootstrap_servers=KAFKA_HOST,
            security_protocol=KAFKA_PROTOCOL,
            sasl_mechanisms=KAFKA_SASL_MECHANISMS,
            sasl_username=KAFKA_USERNAME,
            sasl_password=KAFKA_PASSWORD,
            topic_name=SOURCE_TOPIC_NAME,
        )

        # Connect to Kafka producer
        pipeline_logging.logger.info("Connecting to Kafka producer")
        kafka_producer_client = KafkaProducerClient(
            bootstrap_servers=KAFKA_HOST,
            security_protocol=KAFKA_PROTOCOL,
            sasl_mechanisms=KAFKA_SASL_MECHANISMS,
            sasl_username=KAFKA_USERNAME,
            sasl_password=KAFKA_PASSWORD,
            topic_name=TARGET_TOPIC_NAME,
        )

        # Extract, load, and transform data
        pipeline_logging.logger.info(
            f"Extracting, loading, and transforming data from Kafka topic: '{SOURCE_TOPIC_NAME}' to Kafka topic: '{TARGET_TOPIC_NAME}'"
        )
        extract_load_transform_news_sentiment(
            sentiment_api_client=sentiment_api_client,
            kafka_consumer_client=kafka_consumer_client,
            kafka_producer_client=kafka_producer_client,
        )

        pipeline_logging.logger.info("Pipeline run successful")

    except Exception as e:
        # Log and handle pipeline exceptions
        pipeline_logging.logger.error(f"Pipeline run failed: {e}")


if __name__ == "__main__":
    """
    Runs the pipeline continuously.
    """
    # Load pipeline configuration from YAML file
    yaml_file_path = __file__.replace(".py", ".yaml")
    if Path(yaml_file_path).exists():
        with open(yaml_file_path) as yaml_file:
            pipeline_config = yaml.safe_load(yaml_file)
    else:
        raise Exception(
            f"Missing {yaml_file_path} file! Please create the YAML file with at least a 'name' key for the pipeline name."
        )

    # Initialize PipelineLogging instance
    pipeline_logging = PipelineLogging(
        pipeline_name=pipeline_config.get("name"),
        log_folder_path=pipeline_config.get("config").get("log_folder_path"),
    )

    # Run the pipeline continuously
    while True:
        try:
            pipeline(pipeline_logging=pipeline_logging)
        except BaseException as e:
            # Log and handle pipeline run exceptions
            pipeline_logging.logger.error(
                f"Pipeline run failed. See detailed logs: {e}"
            )
        finally:
            # Wait for the specified duration before starting the next run
            time.sleep(pipeline_config.get("schedule").get("sleep_seconds"))
