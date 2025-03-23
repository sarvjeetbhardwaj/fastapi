from pydantic_settings import BaseSettings

## this module is used to set the environmental variables

class Settings(BaseSettings):
    database_hostname : str
    database_port : str
    database_password : str
    database_name : str
    database_username : str
    secret_key : str
    algorithm : str
    access_token_expire_mins : str

    class Config:
        env_file = '.env'

settings = Settings()