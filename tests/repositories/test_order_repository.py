from decimal import Decimal
from app.domain.entities import Order, OrderStatus


def test_save_new_order(order_repository):
    order = Order(
        user_id = 1,
        total_amount = Decimal("100.00"),
    )
    saved = order_repository.save(order)
    assert saved.id is not None
    assert saved.user_id == 1
    assert saved.status == OrderStatus.CREATED
    assert saved.total_amount == Decimal("100.00")


def test_get_order_by_id(order_repository):
    order = Order(
        user_id = 2,
        total_amount = Decimal("50.00"),
    )
    saved = order_repository.save(order)
    fetched = order_repository.get_by_id(saved.id)
    assert fetched is not None
    assert fetched.id == saved.id
    assert fetched.user_id == 2
    assert fetched.status == OrderStatus.CREATED


def test_update_order_status(order_repository):
    order = Order(
        user_id = 3,
        total_amount = Decimal("75.00"),
    )
    saved = order_repository.save(order)
    saved.mark_paid()
    updated = order_repository.save(saved)
    fetched = order_repository.get_by_id(updated.id)
    assert fetched.status == OrderStatus.PAID


def test_list_orders_by_user(order_repository):
    order_repository.save(
        Order(user_id = 10, total_amount = Decimal("10.00"))
    )
    order_repository.save(
        Order(user_id = 10, total_amount = Decimal("20.00"))
    )
    order_repository.save(
        Order(user_id = 11, total_amount = Decimal("30.00"))
    )
    orders_user_10 = order_repository.list_by_user(10)
    assert len(orders_user_10) == 2
    assert all(o.user_id == 10 for o in orders_user_10)


def test_list_all_orders(order_repository):
    order_repository.save(
        Order(user_id = 20, total_amount = Decimal("5.00"))
    )
    order_repository.save(
        Order(user_id = 21, total_amount = Decimal("15.00"))
    )
    orders = order_repository.list_all()
    assert len(orders) >= 2
