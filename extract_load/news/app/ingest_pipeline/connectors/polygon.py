import requests


class PolygonApiClient:
    def __init__(self, api_key_id: str):
        """
        Initializes the Polygon API client.

        Args:
            api_key_id (str): API key for authentication.
        """
        self.base_url = "https://api.polygon.io/v2/reference"
        if api_key_id is None:
            raise Exception("API key cannot be set to None.")
        self.api_key_id = api_key_id

    def get_news(self, max_timestamp: str, limit: int) -> list[dict]:
        """
        Retrieves news data for all stock tickers.

        Args:
            max_timestamp (str): Threshold timestamp.
            limit (int): Number of news articles to request.

        Returns:
            list[dict]: List of news for all stocks after the maximum timestamp.

        Raises:
            Exception: If response code is not 200.
        """
        url = f"{self.base_url}/news"
        params = {
            "apiKey": self.api_key_id,
            "limit": limit,
            "published_utc.gt": max_timestamp,
            "order": "asc",
            "sort": "published_utc",
        }
        # Send GET request to Polygon API
        response = requests.get(url, params=params)
        # Check if response is successful and has valid data
        if response.status_code == 200 and response.json().get("results") is not None:
            return response.json().get("results")
        else:
            # Raise exception if response is not successful
            raise Exception(
                f"Failed to extract data from Polygon.io API. Status Code: {response.status_code}. Response: {response.text}"
            )
