import datetime
from decimal import Decimal
from typing import List
from .entities import Order
from .exceptions import OrderNotFound
from .repositories import OrderRepository


class OrderDomainService:

    def __init__(self, repo: OrderRepository):
        self.repo = repo


    def create_order(self, user_id: int, total_amount: Decimal) -> Order:
        order = Order(
            user_id = user_id,
            total_amount = total_amount,
            created_at = datetime.datetime.now(datetime.timezone.utc),
        )
        return self.repo.save(order)


    def get_order(self, order_id: int, requester_id: int, requester_role: str) -> Order:
        order = self.repo.get_by_id(order_id)
        if not order:
            raise OrderNotFound()
        if requester_role != "admin" and order.user_id != requester_id:
            raise OrderNotFound()   # ocultar existencia
        return order


    def list_orders(self, requester_id: int, requester_role: str) -> List[Order]:
        if requester_role == "admin":
            return self.repo.list_all()
        return self.repo.list_by_user(requester_id)


    def mark_order_paid(self, order_id: int) -> Order:
        order = self.repo.get_by_id(order_id)
        if not order:
            raise OrderNotFound()
        order.mark_paid()
        return self.repo.save(order)


    def ship_order(self, order_id: int) -> Order:
        order = self.repo.get_by_id(order_id)
        if not order:
            raise OrderNotFound()
        order.ship()
        return self.repo.save(order)


    def cancel_order(self, order_id: int, requester_id: int, requester_role: str) -> Order:
        order = self.repo.get_by_id(order_id)
        if not order:
            raise OrderNotFound()
        order.cancel(requester_id, requester_role)
        return self.repo.save(order)
