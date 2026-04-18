class OrderDomainError(Exception):
    # clase base para todas las excepciones de dominio
    pass


class InvalidOrderState(OrderDomainError):
    pass


class UnauthorizedOrderAction(OrderDomainError):
    pass


class OrderNotFound(OrderDomainError):
    pass
