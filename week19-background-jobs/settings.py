from pathlib import Path
from pydantic import Field,SecretStr
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent/".env",
        extra="ignore"
    )
    mysql_host:str='127.0.0.1'
    mysql_port:int=Field(default=3306,ge=1,le=65535)
    mysql_user:str='root'
    mysql_password:SecretStr
    mysql_database:str='week19_demo'
    redis_broker_url:str='redis://127.0.0.1:6379/1'
    redis_backend_url:str='redis://127.0.0.1:6379/2'

settings = Settings()