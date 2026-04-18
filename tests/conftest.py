import threading
import time
import grpc
import pytest
from app.db.repositories import SqlAlchemyOrderRepository
from app.rpc.server import serve
from tests.domain.fakes import FakeOrderRepository
from app.rpc import order_pb2_grpc
from sqlalchemy.orm import Session
from app.db.session import SessionLocal


@pytest.fixture(scope = "module")
def order_repository_grpc():
    return FakeOrderRepository()


@pytest.fixture(scope = "module")
def grpc_server(order_repository_grpc):
    thread = threading.Thread(
        target = serve,
        kwargs = {
            "repo": order_repository_grpc,
            "port": 50052,
        },
        daemon = True,
    )
    thread.start()
    time.sleep(0.5)
    yield
    # no necesitamos shutdown explicito porque el thread es daemon y pytest termina el proceso


@pytest.fixture()
def grpc_client():
    channel = grpc.insecure_channel("localhost:50052")
    stub = order_pb2_grpc.OrderServiceStub(channel)
    yield stub
    channel.close()


@pytest.fixture()
def db_session():
    # sesion sqlalchemy aislada por test, hace rollback al finalizar
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture()
def order_repository(db_session):
    return SqlAlchemyOrderRepository(db_session)
