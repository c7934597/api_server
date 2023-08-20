import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "127.0.0.1"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="API_SERVER_",
        env_file_encoding="utf-8",
    )

    # max number of threads
    capacity_limiter: int = 40 # Default: 40


    # HTTPAdapter Settings
    # These settings are primarily used to control the behavior of the connection pool.

    # pool_connections: Controls the maximum number of URIs that can be opened at once.
    pool_connections: int = 10  # Default: 10

    # pool_maxsize: The maximum number of connections in the connection pool. When the number of connections reaches this number, new requests will wait until a connection is released.
    pool_maxsize: int = 10      # Default: 10

    # max_retries: The number of times a request should be retried if it fails.
    max_retries: int = 0        # Default: 0 (means no retries)

    # pool_block: Determines if we should block and wait for a connection to be released when the connection pool reaches its maximum.
    pool_block: bool = False     # Default: False (If True, requests will be blocked until a connection becomes available when the pool is full)


    # Request Timeout Settings
    # Set the timeout for connection and reading during a request.

    # connect_timeout: The maximum time to wait for the server to establish a connection.
    connect_timeout: int = 5    # Time to wait for server to establish a connection

    # read_timeout: The maximum time to wait for a server response after sending a request.
    read_timeout: int = 10      # Time to wait on a response after the request has been made


    # Maximum number of concurrently executing jobs. This determines how many jobs can be executed simultaneously.
    max_concurrent_jobs = 5

    # The maximum number of retries when a job fails. If a job fails, it will try again this many times.
    job_max_retries = 3

    # Sleep time in seconds after job failure. This is the amount of time to wait before retrying to execute the job.
    retry_sleep_time_jobs = 5


settings = Settings()
