import uvicorn
from src.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "src.app.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        reload_dirs=["/usr/local/lib/python3.12/site-packages", "/app/src"],
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
