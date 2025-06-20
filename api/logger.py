import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DB_URL = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
engine = create_engine(DB_URL, future=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS chat_logs (
                id SERIAL PRIMARY KEY,
                session_id TEXT,
                prompt TEXT,
                response TEXT,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.commit()

def insert_log(session_id, prompt, response, source="mock"):
    db = SessionLocal()
    db.execute(
        text("""
            INSERT INTO chat_logs (session_id, prompt, response, source)
            VALUES (:session_id, :prompt, :response, :source)
        """),
        {"session_id": session_id, "prompt": prompt, "response": response, "source": source}
    )
    db.commit()
    db.close()

def get_logs(limit):
    db = SessionLocal()
    result = db.execute(text("SELECT * FROM chat_logs ORDER BY created_at DESC LIMIT :limit"), {"limit": limit})
    logs = result.fetchall()
    db.close()
    return [dict(row._mapping) for row in logs]
