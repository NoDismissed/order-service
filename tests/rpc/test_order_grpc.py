import pytest
import grpc
from app.rpc import order_pb2


def test_create_order(grpc_server, grpc_client):
    response = grpc_client.CreateOrder(
        order_pb2.CreateOrderRequest(
            requester_id = 1,
            requester_role = "user",
            total_amount = 100.50,
        )
    )
    order = response.order
    assert order.id > 0
    assert order.user_id == 1
    assert order.status == order_pb2.CREATED
    assert order.total_amount == 100.50


def test_get_order_by_owner(grpc_server, grpc_client):
    create = grpc_client.CreateOrder(
        order_pb2.CreateOrderRequest(
            requester_id = 2,
            requester_role = "user",
            total_amount = 50.00,
        )
    )
    order_id = create.order.id
    response = grpc_client.GetOrder(
        order_pb2.GetOrderRequest(
            order_id = order_id,
            requester_id = 2,
            requester_role = "user",
        )
    )
    assert response.order.id == order_id


def test_get_order_by_other_user_returns_not_found(grpc_server, grpc_client):
    create = grpc_client.CreateOrder(
        order_pb2.CreateOrderRequest(
            requester_id = 3,
            requester_role = "user",
            total_amount = 75.00,
        )
    )
    with pytest.raises(grpc.RpcError) as exc:
        grpc_client.GetOrder(
            order_pb2.GetOrderRequest(
                order_id = create.order.id,
                requester_id = 999,
                requester_role = "user",
            )
        )
    assert exc.value.code() == grpc.StatusCode.NOT_FOUND


def test_cancel_order_by_owner(grpc_server, grpc_client):
    create = grpc_client.CreateOrder(
        order_pb2.CreateOrderRequest(
            requester_id = 4,
            requester_role = "user",
            total_amount = 20.00,
        )
    )
    response = grpc_client.CancelOrder(
        order_pb2.CancelOrderRequest(
            order_id = create.order.id,
            requester_id = 4,
            requester_role = "user",
        )
    )
    assert response.order.status == order_pb2.CANCELLED


def test_cannot_cancel_shipped_order(grpc_server, grpc_client):
    create = grpc_client.CreateOrder(
        order_pb2.CreateOrderRequest(
            requester_id = 5,
            requester_role = "user",
            total_amount = 200.00,
        )
    )
    grpc_client.MarkOrderPaid(
        order_pb2.MarkOrderPaidRequest(
            order_id = create.order.id,
            requester_id = 5,
            requester_role = "admin",
        )
    )
    grpc_client.ShipOrder(
        order_pb2.ShipOrderRequest(
            order_id = create.order.id,
            requester_id = 5,
            requester_role = "admin",
        )
    )
    with pytest.raises(grpc.RpcError) as exc:
        grpc_client.CancelOrder(
            order_pb2.CancelOrderRequest(
                order_id = create.order.id,
                requester_id = 5,
                requester_role = "user",
            )
        )
    assert exc.value.code() == grpc.StatusCode.FAILED_PRECONDITION
