from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    APP_NAME: str = "TaskManager"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_SERVER: str
    MAIL_PORT: int
    REDIS_URL: str
    model_config = SettingsConfigDict(env_file=".env")
    ALLOWED_ORIGINS: str = "http://localhost:5173"
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    SQS_QUEUE_URL: str

settings = Settings()