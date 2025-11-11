# check_db.py
from sqlalchemy import create_engine, text

TEST_DB_URL = "postgresql://testuser:testpass@localhost:5433/test_pharmacy_db"

try:
    engine = create_engine(TEST_DB_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Подключение УСПЕШНО:", result.fetchone())
except Exception as e:
    print("ОШИБКА ПОДКЛЮЧЕНИЯ:", e)