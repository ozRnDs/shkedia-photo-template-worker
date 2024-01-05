from typing import ClassVar
import os
import logging
logging.basicConfig(format='%(asctime)s.%(msecs)05d | %(levelname)s | %(filename)s:%(lineno)d | %(message)s' , datefmt='%FY%T')

from pydantic_settings import BaseSettings

class ApplicationConfiguration(BaseSettings):

    RECONNECT_WAIT_TIME: int = 1
    RETRY_NUMBER: int = 10
    ENVIRONMENT: str = "dev0"
    DEBUG: bool = False
    LOG_LEVEL: int = 30

    # Authentication Configuration values
    AUTH_SERVICE_URL: str = "CHANGE ME"

    # DB Configuration values
    AUTH_DB_CREDENTIALS_LOCATION: str = "/temp/postgres_credentials/postgres_credentials.json"

    # DB Configuration values
    MEDIA_DB_HOST: str = "10.0.0.5"
    MEDIA_DB_PORT: str = "4431"
    MEDIA_REPO_HOST: str = "10.0.0.5"
    MEDIA_REPO_PORT: str = "4432"
    USER_DB_HOST: str = "10.0.0.5"
    USER_DB_PORT: str = "4430"
        
    # Encryption Configuration Values
    PUBLIC_KEY_LOCATION: str = ".local/data.pub"
    PRIVATE_KEY_LOCATION: str = ".local/data"

    # Worker Configuration Values
    ENGINE_NAME: str = "template-worker"
    DESCRIPTION: str = "Template for a worker component"
    INPUT_SOURCE: str = "NOT SET"
    INPUT_QUEUE_NAME: str = "NOT SET"
    OUTPUT_EXCHANGE_NAME: str = "NOT SET"
    
    BATCH_SIZE: int = 100
    BATCH_PROCESS_PERIOD_MIN: float = 30

    logger: ClassVar[logging.Logger]= logging.getLogger()


app_config = ApplicationConfiguration()
app_config.logger.setLevel(app_config.LOG_LEVEL)
app_config.logger.info("Loaded Application Configuration")