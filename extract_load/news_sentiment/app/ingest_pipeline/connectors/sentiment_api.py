import requests


class SentimentApiClient:
    def __init__(self, url: str):
        """
        Initializes a SentimentApiClient instance.

        Args:
            url (str): The base URL of the Sentiment API.

        Raises:
            Exception: If the provided URL is None.
        """
        if url is None:
            raise Exception("URL cannot be set to None.")
        self.base_url = url

    def get_sentiment(self, q: str):
        """
        Retrieves sentiment analysis for the specified text.

        Args:
            q (str): The text for which sentiment analysis is requested.

        Returns:
            tuple: A tuple containing sentiment label and score.

        Raises:
            Exception: If the response code is not 200.
        """
        # Fetch data from the Sentiment API
        params = {"q": q}
        response = requests.get(f"{self.base_url}/sentiment", params=params)
        if response.status_code == 200:
            response_json = response.json()
            return response_json.get("label"), response_json.get("score")
        else:
            raise Exception(
                f"Failed to extract data from Sentiment API. Status Code: {response.status_code}. Response: {response.text}"
            )
