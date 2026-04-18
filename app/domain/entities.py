from dataclasses import dataclass
import datetime
from decimal import Decimal
from typing import Optional
from .exceptions import InvalidOrderState, UnauthorizedOrderAction
from .enums import OrderStatus


@dataclass
class Order:
    user_id: int
    total_amount: Decimal
    status: OrderStatus = OrderStatus.CREATED
    created_at: datetime = datetime.datetime.now(datetime.timezone.utc)
    id: Optional[int] = None

    # comportamiento del dominio
    def mark_paid(self):
        if self.status != OrderStatus.CREATED:
            raise InvalidOrderState(f"Cannot mark order as PAID from {self.status}")
        self.status = OrderStatus.PAID


    def ship(self):
        if self.status != OrderStatus.PAID:
            raise InvalidOrderState(f"Cannot ship order from {self.status}")
        self.status = OrderStatus.SHIPPED


    def cancel(self, requester_id: int, requester_role: str):
        if self.status == OrderStatus.SHIPPED:
            raise InvalidOrderState("Cannot cancel a shipped order")
        if requester_role != "admin" and requester_id != self.user_id:
            raise UnauthorizedOrderAction("Only owner or admin can cancel this order")
        self.status = OrderStatus.CANCELLED
