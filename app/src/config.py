import os

def get_database_url() -> str:
    # docker-compose będzie podawał DATABASE_URL
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    # fallback lokalny (gdybyś odpalał bez Compose)
    return "postgresql+psycopg2://postgres:postgres@localhost:5432/appdb"