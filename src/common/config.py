from pydantic_settings import BaseSettings
from pydantic import Field, IPvAnyAddress, SecretStr, FilePath, DirectoryPath
from typing import Annotated

class BotSettings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ADMIN_ID: int
    USE_REDIS: bool = False
    

class DatabaseSettings(BaseSettings):
    DB_HOST: IPvAnyAddress
    DB_PORT: Annotated[int, Field(ge=1, le=65535)] = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: SecretStr = 'unknown'
    
    SSH_HOST: IPvAnyAddress
    SSH_PORT: Annotated[int, Field(ge=1, le=65535)] = 22
    SSH_USERNAME: str = 'username'
    SSH_KEY_PATH: FilePath = 'local\ssh\path'
    SSH_KEY_PASSPHRASE: SecretStr = 'unknown'

    SERVER_PHOTO_DIR_PATH: str

class Settings(BaseSettings):
    bot: BotSettings = BotSettings()
    db: DatabaseSettings = DatabaseSettings()
    debug: bool = False
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'

config = Settings()