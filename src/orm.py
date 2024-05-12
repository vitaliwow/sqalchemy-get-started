from sqlalchemy import select, update, func, cast, Integer, and_

from src.database import sync_engine, session_factory, async_session_factory, async_engine
from src.models import metadata, WorkerORM, ResumeORM


class SyncORM:

    def __init__(self) -> None:
        self.delete_tables()
        self.create_tables()
        self.insert_data()

    @staticmethod
    def delete_tables() -> None:
        metadata.echo = False
        metadata.drop_all(sync_engine)
        metadata.echo = True

    @staticmethod
    def create_tables() -> None:
        metadata.create_all(sync_engine)

    @staticmethod
    def insert_data() -> None:
        worker1 = WorkerORM(username="user1")
        worker2 = WorkerORM(username="user2")
        resume1 = ResumeORM(title="title1", compensation=1000, workload="fulltime", worker_id=1)
        resume2 = ResumeORM(title="title2", compensation=2000, workload="parttime", worker_id=2)

        with session_factory() as session:
            session.add_all([worker1, worker2])
            session.commit()
            session.add_all([resume1, resume2])
            session.commit()

    @staticmethod
    def select_workers() -> None:
        with session_factory() as session:
            query = select(WorkerORM)
            result = session.execute(query)
            print(result.scalars().all())

    @staticmethod
    def update_worker() -> None:
        with session_factory() as session:
            worker_1 = session.get(WorkerORM, 1)
            worker_1.username = "user14"
            session.commit()

    @staticmethod
    def select_resume() -> None:
        with session_factory() as session:
            query = (
                select(
                    ResumeORM.workload,
                    cast(func.avg(ResumeORM.compensation).label("average_compensation"), Integer).label("average_compensation")
                )
                .select_from(ResumeORM)
                .filter(and_(ResumeORM.title.contains("title"), ResumeORM.compensation > 1000))
                .group_by(ResumeORM.workload)
                .having(func.avg(ResumeORM.compensation) > 1500)
            )
            # print(query.compile(compile_kwargs={"literal_binds": True}))
            result = session.execute(query)
            res = result.all()
            print(res[0].average_compensation)


async def async_insert_data() -> None:
    worker1 = WorkerORM(username="user1")
    worker2 = WorkerORM(username="user3")

    async with async_session_factory() as session:
        session.add(worker1)
        session.add(worker2)
        await session.commit()
