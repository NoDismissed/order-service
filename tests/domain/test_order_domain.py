from decimal import Decimal
import pytest
from app.domain.enums import OrderStatus
from app.domain.services import OrderDomainService
from tests.domain.fakes import FakeOrderRepository


def test_user_can_cancel_own_order():
    repo = FakeOrderRepository()
    service = OrderDomainService(repo)
    order = service.create_order(user_id = 1, total_amount = Decimal("100.00"))
    cancelled = service.cancel_order(
        order_id = order.id,
        requester_id = 1,
        requester_role = "user",
    )
    assert cancelled.status == OrderStatus.CANCELLED


def test_user_cannot_cancel_other_users_order():
    repo = FakeOrderRepository()
    service = OrderDomainService(repo)
    order = service.create_order(user_id = 1, total_amount = Decimal("50.00"))
    with pytest.raises(Exception):
        service.cancel_order(
            order_id = order.id,
            requester_id = 2,
            requester_role = "user",
        )


def test_admin_can_cancel_any_order():
    repo = FakeOrderRepository()
    service = OrderDomainService(repo)
    order = service.create_order(user_id = 1, total_amount = Decimal("80.00"))
    cancelled = service.cancel_order(
        order_id = order.id,
        requester_id = 999,
        requester_role = "admin",
    )
    assert cancelled.status == OrderStatus.CANCELLED
