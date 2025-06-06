import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


def print_usage():
    print("Usage: python main.py <database_name>")
    sys.exit(1)


def init_database(db_name: str):
    engine = create_engine(f"sqlite:///{db_name}.db", echo=False)
    Session = sessionmaker(bind=engine, autoflush=False)
    Base.metadata.create_all(engine)
    return engine, Session


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_usage()

    db_name = sys.argv[1]
    engine, Session = init_database(db_name)
