from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Order


class OrderRepository(ABC):

    @abstractmethod
    def save(self, order: Order) -> Order:
        pass


    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        pass


    @abstractmethod
    def list_by_user(self, user_id: int) -> List[Order]:
        pass


    @abstractmethod
    def list_all(self) -> List[Order]:
        pass
