from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from app.domain.entities import Order, OrderStatus
from app.domain.repositories import OrderRepository
from app.db.models import OrderModel


class SqlAlchemyOrderRepository(OrderRepository):

    def __init__(self, session: Session):
        self.session = session


    def save(self, order: Order) -> Order:
        if order.id is None:
            model = OrderModel(
                user_id = order.user_id,
                status = order.status.value,
                total_amount = order.total_amount,
                created_at = order.created_at,
            )
            self.session.add(model)
            self.session.commit()
            order.id = model.id
        else:
            model = self.session.get(OrderModel, order.id)
            model.status = order.status.value
            self.session.commit()
        return order


    def get_by_id(self, order_id: int) -> Optional[Order]:
        model = self.session.get(OrderModel, order_id)
        if not model:
            return None
        return Order(
            id = model.id,
            user_id = model.user_id,
            status = OrderStatus(model.status),
            total_amount = Decimal(model.total_amount),
            created_at = model.created_at,
        )


    def list_by_user(self, user_id: int) -> List[Order]:
        models = (
            self.session.query(OrderModel)
            .filter(OrderModel.user_id == user_id)
            .all()
        )
        return [self._to_domain(m) for m in models]


    def list_all(self) -> List[Order]:
        models = self.session.query(OrderModel).all()
        return [self._to_domain(m) for m in models]


    def _to_domain(self, model: OrderModel) -> Order:
        return Order(
            id = model.id,
            user_id = model.user_id,
            status = OrderStatus(model.status),
            total_amount = Decimal(model.total_amount),
            created_at = model.created_at,
        )
