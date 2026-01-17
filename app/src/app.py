import os
from flask import Flask, jsonify, request
from sqlalchemy import text
from .config import get_database_url
from .db import make_engine, make_session_factory
from .models import Base, User

def create_app() -> Flask:
    app = Flask(__name__)

    database_url = get_database_url()
    engine = make_engine(database_url)
    SessionLocal = make_session_factory(engine)

    @app.get("/health")
    def health():
        # sprawdzamy DB prostym SELECT 1
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return jsonify(status="ok", db="ok")
        except Exception as e:
            return jsonify(status="degraded", db="error", error=str(e)), 500

    @app.get("/users")
    def list_users():
        with SessionLocal() as session:
            users = session.query(User).order_by(User.id.asc()).all()
            return jsonify([
                {"id": u.id, "email": u.email, "name": u.name}
                for u in users
            ])

    @app.post("/users")
    def create_user():
        payload = request.get_json(force=True, silent=True) or {}
        email = payload.get("email")
        name = payload.get("name")

        if not email or not name:
            return jsonify(error="email and name are required"), 400

        with SessionLocal() as session:
            u = User(email=email, name=name)
            session.add(u)
            session.commit()
            session.refresh(u)
            return jsonify({"id": u.id, "email": u.email, "name": u.name}), 201

    @app.get("/version")
    def version():
        return jsonify(version=os.getenv("APP_VERSION", "dev"))

    return app

# dla gunicorn: "app.src.app:create_app()"