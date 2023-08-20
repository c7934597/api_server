import requests
from requests.adapters import HTTPAdapter

from loguru import logger
from api_server.settings import settings


class Requests_Handler:
    def __init__(self) -> None:
        self.session = requests.Session()

        # Customize the connection pool's cache size and maximum size
        adapter = HTTPAdapter(pool_connections=settings.pool_connections, pool_maxsize=settings.pool_maxsize, max_retries=settings.max_retries, pool_block=settings.pool_block)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def post_request(self, url: str, headers: dict = None, json_data: dict = None, timeout: tuple = (settings.connect_timeout, settings.read_timeout)) -> requests.Response:
        """
        Send a POST request to the specified URL.

        Parameters:
        - url: The target URL.
        - headers: The headers to be sent with the request.
        - json_data: The JSON data to be sent as the body of the request.
        - timeout: A tuple indicating the connect and read timeouts.

        Returns:
        - The response object or None if there's an exception.
        """
        return self._request("POST", url, headers=headers, json=json_data, timeout=timeout)

    def get_request(self, url: str, headers: dict = None, params: dict = None, timeout: tuple = (5, 10)) -> requests.Response:
        """
        Send a GET request to the specified URL.

        Parameters:
        - url: The target URL.
        - headers: The headers to be sent with the request.
        - params: The query parameters to be sent with the request.
        - timeout: A tuple indicating the connect and read timeouts.

        Returns:
        - The response object or None if there's an exception.
        """
        return self._request("GET", url, headers=headers, params=params, timeout=timeout)

    def _request(self, method: str, url: str, headers: dict = None, json: dict = None, params: dict = None, timeout: tuple = (5, 10)) -> requests.Response:
        """
        A private method to handle HTTP requests. This method consolidates the common logic for sending GET and POST requests.

        Parameters:
        - method: The HTTP method (GET, POST, etc.).
        - url: The target URL.
        - headers: The headers to be sent with the request.
        - json: The JSON data to be sent as the body of the request (relevant for POST requests).
        - params: The query parameters to be sent with the request (relevant for GET requests).
        - timeout: A tuple indicating the connect and read timeouts.

        Returns:
        - The response object or None if there's an exception.
        """
        try:
            response = self.session.request(method, url, headers=headers, json=json, params=params, timeout=timeout)

            if 200 <= response.status_code < 300:
                logger.debug(f"Request to {url} using {method} was successful with status code: {response.status_code}")
            else:
                logger.error(f"Request to {url} using {method} failed with status code: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Request to {url} using {method} encountered an exception: {e}")
            return None
