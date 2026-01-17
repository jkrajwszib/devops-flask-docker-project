import os

def get_database_url() -> str:

    url = os.getenv("DATABASE_URL")
    if url:
        return url

    return "postgresql+psycopg2://postgres:postgres@localhost:5432/appdb"
