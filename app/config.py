import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

@dataclass
class DatabaseConfig:
    host: str = os.getenv("POSTGRES_HOST", "db")
    port: int = int(os.getenv("POSTGRES_PORT", 5432))
    database: str = os.getenv("POSTGRES_DB", "chatbot")
    user: str = os.getenv("POSTGRES_USER", "postgres")
    password: str = os.getenv("POSTGRES_PASSWORD", "your_secure_password")

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

@dataclass
class APIConfig:
    base_url: str = os.getenv("OPENAI_BASE_URL", "https://llama3gpu.neuraldeep.tech/v1")
    model: str = os.getenv("OPENAI_MODEL", "llama-3-8b-instruct-8k")

@dataclass
class AppConfig:
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

@dataclass
class Config:
    db: DatabaseConfig = DatabaseConfig()
    api: APIConfig = APIConfig()
    app: AppConfig = AppConfig()

# Создаем экземпляр конфигурации
config = Config() 