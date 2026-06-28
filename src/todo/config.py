from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    todo_db_path: str = "todos.json"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
