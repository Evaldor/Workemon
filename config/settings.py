from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost/workemon_db"
    elasticsearch_url: str = "http://localhost:9200"
    llm_provider: str = "yandex"
    saved_prompt: str = "Process this request:"
    yandex_imap_server: str = "imap.yandex.com"
    yandex_username: str = ""
    yandex_password: str = ""
    telegram_bot_token: str = ""
    yandex_gpt_api_key: str = ""
    deepseek_api_key: str = ""
    grok_api_key: str = ""
    jira_url: str = ""
    jira_username: str = ""
    jira_password: str = ""
    jira_project_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()