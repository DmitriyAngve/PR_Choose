from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings


# Создаю объект, который будет знать куда и как подключаться БД с помощью SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL
)

# Создаю функцию, которая возвращает новые SQLAlchemy-сессии, привязанные к моему объекту engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Объявляю базовый класс, от которого будут наследоваться все ORM-модели
Base = declarative_base()

# get_db() - это функция-зависимость, которая создает и закрывает сессию к БД
# db = SessionLocal() - создает новую сессию
# yield db - даёт доступ к сессии в endpoint
# finally: db.close() - гарантирует закрытие сессии даже при ошибках
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Base.metadata - содержит информацию о всех моделях, которые я создаю и унаследую от Base
# create_all(bind=engine) - команда для создания всех таблиц в БД, используя подключение engine, если таких таблиц еще нет
def create_tables():
    Base.metadata.create_all(bind=engine)