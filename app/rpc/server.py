from concurrent import futures
import grpc
from app.db.repositories import SqlAlchemyOrderRepository
from app.db.session import SessionLocal
from app.rpc import order_pb2_grpc
from app.rpc.handlers import OrderGrpcHandler
from app.domain.services import OrderDomainService
from app.domain.repositories import OrderRepository
from app.config import ORDER_SERVICE_PORT


def serve(repo: OrderRepository, port: int = 50052):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers = 10)
    )
    service = OrderDomainService(repo)
    handler = OrderGrpcHandler(service)
    order_pb2_grpc.add_OrderServiceServicer_to_server(
        handler, server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Order gRPC server running on port {port}")
    server.wait_for_termination()


def main():
    port = ORDER_SERVICE_PORT
    session = SessionLocal()
    repo = SqlAlchemyOrderRepository(session)
    serve(repo, port = port)


if __name__ == "__main__":
    main()
