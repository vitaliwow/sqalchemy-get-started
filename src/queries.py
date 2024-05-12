from sqlalchemy import insert, select, update

from database import sync_engine
from models import metadata, workers


def delete_tables() -> None:
    metadata.echo = False
    metadata.drop_all(sync_engine)
    metadata.echo = True


def create_tables() -> None:
    metadata.create_all(sync_engine)


def insert_data() -> None:
    with sync_engine.connect() as connection:
        statement = insert(workers).values([
            {"username": "user1"},
            {"username": "user2"},
            {"username": "user3"},
        ])
        connection.execute(statement)
        connection.commit()


def select_data() -> None:
    with sync_engine.connect() as connection:
        query = select(workers)
        result = connection.execute(query)
        print(result.fetchall())


def update_data() -> None:
    with sync_engine.connect() as connection:
        query = (
            update(workers)
            .filter_by(username="user2")
            .values(username="user24")
        )
        connection.execute(query)
        connection.commit()


if __name__ == "__main__":
    update_data()
    select_data()

