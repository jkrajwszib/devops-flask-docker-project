from sqlalchemy import text
from src.config import get_database_url
from src.db import make_engine
from src.models import Base

def main():
    engine = make_engine(get_database_url())

    # szybki check, czy DB żyje
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    # minimalne "migracje" w wersji projektu: create_all
    Base.metadata.create_all(bind=engine)
    print("Migrations applied (create_all).")

if __name__ == "__main__":
    main()