import os
import sys

from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from os import getenv
from typing import Optional

from sqlalchemy import URL

load_dotenv()


@dataclass
class DatabaseConfig:
    """Dependencies for database connection"""
    
    database: Optional[str] = getenv('DATABASE_NAME')
    username: Optional[str] = getenv('DATABASE_USERNAME')
    password: Optional[str] = getenv('DATABASE_PASSWORD')
    host: Optional[str] = getenv('DATABASE_HOST')
    port: int = int(getenv('DATABASE_PORT', 5432))

    debug: bool = getenv('DATABASE_DEBUG', 'False') == 'True'

    driver: Optional[str] = getenv('DATABASE_DRIVER')
    dialect: Optional[str] = getenv('DATABASE_DIALECT')


    def create_connection_url(self) -> str:
        """Create a connection string"""

        return URL.create(
            drivername=f'{self.dialect}+{self.driver}',
            username=self.username,
            database=self.database,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)

@dataclass
class BotConfig:
    """Settings of telegram-bot"""

    BOT_TOKEN: str = getenv('BOT_TOKEN', '')
    LOGGING_LEVEL:int = int(getenv('LOGGING_LEVEL', 1))
    THROTTLING_LIMIT: int = int(getenv('THROTTLING_LIMIT', 5))
    

@dataclass
class AppSettings:
    """
    Base class that combines all configs in itself. All settings are
    in the BASE_DIR -> .env
    """

    db = DatabaseConfig()
    bot = BotConfig()

settings = AppSettings()
