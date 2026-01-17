import csv
import json
import os
from datetime import datetime

from sqlalchemy import text
from src.config import get_database_url
from src.db import make_engine, make_session_factory
from src.models import User

SEED_DIR = os.getenv("SEED_DIR", "/seed_output")


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def main():
    engine = make_engine(get_database_url())
    SessionLocal = make_session_factory(engine)

    # sprawdzenie połączenia
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    ensure_dir(SEED_DIR)

    users_to_create = [
        ("alice@example.com", "Alice"),
        ("bob@example.com", "Bob"),
        ("carol@example.com", "Carol"),
        ("dave@example.com", "Dave"),
        ("eve@example.com", "Eve"),
    ]

    created = []

    with SessionLocal() as session:
        for email, name in users_to_create:
            existing = session.query(User).filter(User.email == email).first()
            if existing:
                continue
            u = User(email=email, name=name)
            session.add(u)
            created.append(u)

        session.commit()

        for u in created:
            session.refresh(u)

        all_users = session.query(User).order_by(User.id.asc()).all()

    # seed.log
    log_path = os.path.join(SEED_DIR, "seed.log")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(
            f"[{datetime.utcnow().isoformat()}Z] "
            f"Seed executed. Total users={len(all_users)}\n"
        )

    # users.csv
    csv_path = os.path.join(SEED_DIR, "users.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "email", "name"])
        for u in all_users:
            writer.writerow([u.id, u.email, u.name])

    # data.json
    json_path = os.path.join(SEED_DIR, "data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            [{"id": u.id, "email": u.email, "name": u.name} for u in all_users],
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Seed completed. Files written to {SEED_DIR}")


if __name__ == "__main__":
    main()