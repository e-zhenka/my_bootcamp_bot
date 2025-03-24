import psycopg2
from psycopg2.extras import DictCursor
from app.config import config

class DatabaseManager:
    def __init__(self):
        self.init_db()

    def get_db_connection(self):
        return psycopg2.connect(
            dbname=config.db.database,
            user=config.db.user,
            password=config.db.password,
            host=config.db.host,
            port=config.db.port
        )

    def init_db(self):
        """Инициализация базы данных"""
        retries = 5  # Количество попыток подключения
        for attempt in range(retries):
            try:
                with self.get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            CREATE TABLE IF NOT EXISTS chat_messages (
                                id SERIAL PRIMARY KEY,
                                session_id VARCHAR(100),
                                role VARCHAR(50),
                                content TEXT,
                                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        """)
                        conn.commit()
                return  # Если успешно, выходим из функции
            except psycopg2.Error as e:
                if attempt == retries - 1:  # Если это последняя попытка
                    raise Exception(f"Не удалось инициализировать базу данных после {retries} попыток: {str(e)}")
                import time
                time.sleep(1)  # Ждем 1 секунду перед следующей попыткой

    def save_message(self, session_id: str, role: str, content: str) -> None:
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO chat_messages (session_id, role, content) VALUES (%s, %s, %s)",
                    (session_id, role, content)
                )
                conn.commit()

    def load_chat_history(self, session_id: str) -> list:
        try:
            with self.get_db_connection() as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    cur.execute(
                        "SELECT role, content FROM chat_messages WHERE session_id = %s ORDER BY timestamp",
                        (session_id,)
                    )
                    return [{"role": row["role"], "content": row["content"]} for row in cur.fetchall()]
        except psycopg2.Error as e:
            print(f"Ошибка при загрузке истории чата: {str(e)}")
            return []

    def clear_chat_history(self, session_id: str) -> None:
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM chat_messages WHERE session_id = %s", (session_id,))
                conn.commit() 