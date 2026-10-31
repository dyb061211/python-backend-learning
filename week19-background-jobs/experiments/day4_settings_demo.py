from pydantic import Field,SecretStr
from pydantic_settings import BaseSettings,SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    mysql_host:str="127.0.0.1"
    mysql_port:int=Field(default=3306,ge=1,le=65535)
    mysql_password:SecretStr

if __name__ == "__main__":
    settings = Settings()
    print("Host:", settings.mysql_host)
    print("Port:", settings.mysql_port)
    print("Port type:", type(settings.mysql_port))
    print("Password configured:", bool(settings.mysql_password.get_secret_value()))
    print(type(os.environ["MYSQL_PORT"]))
    print(type(settings.mysql_port))