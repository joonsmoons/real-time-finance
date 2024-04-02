from dotenv import load_dotenv
import os
from pathlib import Path
from ingest_pipeline.connectors.polygon import PolygonApiClient
from ingest_pipeline.connectors.kafka import KafkaClient
from ingest_pipeline.assets.pipeline_logging import PipelineLogging
from ingest_pipeline.assets.polygon import extract_load_polygon_indicies
import yaml
import time
import asyncio


def pipeline(config: dict, pipeline_logging: PipelineLogging):
    """
    Main pipeline function that orchestrates data extraction and loading.

    Args:
        config (dict): Configuration settings for the pipeline.
        pipeline_logging (PipelineLogging): Instance of PipelineLogging for logging.

    Raises:
        Exception: If any error occurs during the pipeline execution.
    """
    pipeline_logging.logger.info("Starting pipeline run")

    # set up environment variables
    pipeline_logging.logger.info("Getting pipeline environment variables")
    API_KEY_ID = os.environ.get("POLYGON_API_KEY")
    KAFKA_HOST = os.environ.get("bootstrap_servers")
    KAFKA_PROTOCOL = os.environ.get("security_protocol")
    KAFKA_SASL_MECHANISMS = os.environ.get("sasl_mechanisms")
    KAFKA_USERNAME = os.environ.get("sasl_username")
    KAFKA_PASSWORD = os.environ.get("sasl_password")
    KAFKA_TOPIC_NAME = os.environ.get("kafka_indicies_topic_name")

    pipeline_logging.logger.info("Creating Polygon.io API client")
    polygon_client = PolygonApiClient(api_key_id=API_KEY_ID)

    pipeline_logging.logger.info("Connecting to Kafka producer")
    kafka_client = KafkaClient(
        bootstrap_servers=KAFKA_HOST,
        security_protocol=KAFKA_PROTOCOL,
        sasl_mechanisms=KAFKA_SASL_MECHANISMS,
        sasl_username=KAFKA_USERNAME,
        sasl_password=KAFKA_PASSWORD,
        topic_name=KAFKA_TOPIC_NAME,
    )

    # extract from Polygon API
    pipeline_logging.logger.info(
        f"Extracting and loading data from Polygon.io API to Kafka topic: {KAFKA_TOPIC_NAME}"
    )
    asyncio.run(
        extract_load_polygon_indicies(
            polygon_client=polygon_client,
            kafka_client=kafka_client,
            time_threshold=config.get("time_threshold"),
        )
    )

    pipeline_logging.logger.info("Pipeline run successful")


if __name__ == "__main__":
    """
    Runs the pipeline continuously.
    """
    load_dotenv()
    yaml_file_path = __file__.replace(".py", ".yaml")
    if Path(yaml_file_path).exists():
        with open(yaml_file_path) as yaml_file:
            pipeline_config = yaml.safe_load(yaml_file)
    else:
        raise Exception(
            f"Missing {yaml_file_path} file! Please create the yaml file with at least a `name` key for the pipeline name."
        )

    pipeline_logging = PipelineLogging(
        pipeline_name=pipeline_config.get("name"),
        log_folder_path=pipeline_config.get("config").get("log_folder_path"),
    )

    while True:
        try:
            pipeline(
                config=pipeline_config.get("config"), pipeline_logging=pipeline_logging
            )
        except BaseException as e:
            pipeline_logging.logger.error(
                f"Pipeline run failed. See detailed logs: {e}"
            )
        finally:
            time.sleep(pipeline_config.get("schedule").get("sleep_seconds"))
