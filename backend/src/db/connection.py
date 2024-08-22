from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.schema import CreateSchema, CreateTable
from sqlalchemy.exc import ProgrammingError
from yarl import URL
from src.db.base import Base
import asyncpg
import psycopg2
from src.config import config

POSTGRES_HOST = config.db["POSTGRES_HOST"]
POSTGRES_PORT = config.db["POSTGRES_PORT"]
POSTGRES_USER = config.db["POSTGRES_USER"]
POSTGRES_PASSWORD = config.db["POSTGRES_PASSWORD"]
POSTGRES_DB = config.db["POSTGRES_DB"]
POSTGRES_SCHEMA: str = config.db["POSTGRES_SCHEMA"]
POSTGRES_DB_echo: bool = False

def db_url() -> URL:
    """
    Assemble database URL from settings.

    :return: database URL.
    """
    return URL.build(
        scheme="postgresql+asyncpg",
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        path=f"/{POSTGRES_DB}",
    )


DATABASE_URL = db_url()
engine = create_async_engine(str(DATABASE_URL), echo=True)


# AsyncSessionLocal = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )

async def init_db():
    # async with engine.begin() as conn:
        # Create schema if it does not exist
        # try:
        #     await conn.execute(CreateSchema(POSTGRES_SCHEMA))
        # except ProgrammingError:
        #     pass  # Schema already exists

        # Create tables
        # try:
        #     await conn.run_sync(Base.metadata.create_all)
        #     print("Tables created successfully.")
        # except Exception as e:
        #     print(f"Error creating tables: {e}")

    pass


def get_connection():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        connect_timeout=20,
    )
    return conn

pool = None


async def create_db_pool():
    try:
        global pool
        pool = await asyncpg.create_pool(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            min_size=1,
            max_size=5,
        )
        print("Database connection pool created successfully.")
        size = pool.get_size()
        print("pool_size :", size)

    except Exception as e:
        print(f"Error while creating database connection pool:", e)


async def close_db_pool():
    global pool
    if pool:
        await pool.close()
        print("Database connection pool closed successfully.")


async def aget_connection():
    try:
        global pool
        if pool is None:
            await create_db_pool()
        conn = await pool.acquire()
        print("Successfully received a database connection from the connection pool.")
        return conn
    except Exception as e:
        print(f"Error while creating database connection: {e}")


async def release_connection(conn):
    try:
        global pool
        await pool.release(conn)
        print("Connection released back to the pool.")
    except Exception as e:
        print(f"Error releasing connection back to the pool: {e}")
