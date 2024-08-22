import taskiq_fastapi
from src.settings import settings
from taskiq import InMemoryBroker

if settings.environment.lower() == "pytest":
    broker = InMemoryBroker()

taskiq_fastapi.init(
    broker,
    "src.app.application:get_app",
)
