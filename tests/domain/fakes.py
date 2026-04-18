from typing import Dict, List, Optional
from app.domain.entities import Order
from app.domain.repositories import OrderRepository


class FakeOrderRepository(OrderRepository):

    def __init__(self):
        self._orders: Dict[int, Order] = {}
        self._next_id = 1


    def save(self, order: Order) -> Order:
        if order.id is None:
            order.id = self._next_id
            self._next_id += 1
        self._orders[order.id] = order
        return order


    def get_by_id(self, order_id: int) -> Optional[Order]:
        return self._orders.get(order_id)


    def list_by_user(self, user_id: int) -> List[Order]:
        return [o for o in self._orders.values() if o.user_id == user_id]


    def list_all(self) -> List[Order]:
        return list(self._orders.values())
