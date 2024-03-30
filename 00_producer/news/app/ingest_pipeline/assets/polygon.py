from pathlib import Path
import os
from ingest_pipeline.connectors.polygon import PolygonApiClient
from ingest_pipeline.connectors.kafka import KafkaClient


def extract_max_timestamp(max_timestamp_path: Path) -> str:
    """
    Extracts the maximum timestamp from the given file path.

    Args:
        max_timestamp_path (Path): Path to the file containing the maximum timestamp.
        default_max_timestamp (str): Default maximum timestamp value.

    Returns:
        str: The maximum timestamp extracted from the file or the default value if the file doesn't exist.
    """
    with open(max_timestamp_path, "r") as f:
        max_timestamp = f.read().strip()
        return max_timestamp


def update_max_timestamp(timestamp: str, max_timestamp_path: Path) -> None:
    """
    Updates the maximum timestamp in the specified file path.

    Args:
        timestamp (str): The timestamp to update.
        max_timestamp_path (Path): Path to the file containing the maximum timestamp.
    """
    with open(max_timestamp_path, "w") as f:
        f.write(timestamp)


def extract_polygon_news(
    polygon_client: PolygonApiClient, max_timestamp_path: Path, limit: int = 10
) -> list[dict]:
    """
    Extracts news data from Polygon API since the last timestamp stored in the file.

    Args:
        polygon_client (PolygonApiClient): Instance of Polygon API client.
        max_timestamp_path (Path): Path to the file containing the maximum timestamp.
        limit (int, optional): Maximum number of news articles to retrieve. Defaults to 10.

    Returns:
        list[dict]: List of news articles retrieved from the Polygon API.
    """
    max_timestamp = extract_max_timestamp(max_timestamp_path=max_timestamp_path)
    data = polygon_client.get_news(max_timestamp=max_timestamp, limit=limit)
    if len(data) > 0:
        update_max_timestamp(
            timestamp=data[-1].get("published_utc"),
            max_timestamp_path=max_timestamp_path,
        )
    return data


def load_polygon_news(kafka_client: KafkaClient, data: list[dict]) -> None:
    """
    Loads news data into a Kafka producer.

    Args:
        kafka_client (KafkaClient): Instance of Kafka client.
        data (list[dict]): List of news articles to be loaded into Kafka.
    """
    kafka_client.produce(data)
