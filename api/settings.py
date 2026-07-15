from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TELEGRAM_", case_sensitive=False)

    bot_token: str
    chat_id: str


telegram_settings = TelegramSettings()
