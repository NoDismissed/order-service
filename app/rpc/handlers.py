import grpc
from app.domain.services import OrderDomainService
from app.domain.exceptions import OrderNotFound, InvalidOrderState, UnauthorizedOrderAction
from app.rpc import order_pb2
from app.rpc import order_pb2_grpc


class OrderGrpcHandler(order_pb2_grpc.OrderServiceServicer):

    def __init__(self, service: OrderDomainService):
        self.service = service


    def _to_proto(self, order):
        return order_pb2.Order(
            id = order.id,
            user_id = order.user_id,
            status = order_pb2.OrderStatus.Value(order.status.name),
            total_amount = float(order.total_amount),
            created_at = order.created_at.isoformat(),
        )


    def CreateOrder(self, request, context):
        try:
            order = self.service.create_order(
                user_id = request.requester_id,
                total_amount = request.total_amount,
            )
            return order_pb2.CreateOrderResponse(
                order = self._to_proto(order)
            )
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))


    def GetOrder(self, request, context):
        try:
            order = self.service.get_order(
                order_id = request.order_id,
                requester_id = request.requester_id,
                requester_role = request.requester_role,
            )
            return order_pb2.GetOrderResponse(
                order = self._to_proto(order)
            )
        except OrderNotFound:
            context.abort(grpc.StatusCode.NOT_FOUND, "Order not found")
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))


    def ListOrders(self, request, context):
        try:
            orders = self.service.list_orders(
                requester_id = request.requester_id,
                requester_role = request.requester_role,
            )
            return order_pb2.ListOrdersResponse(
                orders = [self._to_proto(o) for o in orders]
            )
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))


    def MarkOrderPaid(self, request, context):
        try:
            order = self.service.mark_order_paid(
                order_id = request.order_id
            )
            return order_pb2.MarkOrderPaidResponse(
                order = self._to_proto(order)
            )
        except OrderNotFound:
            context.abort(grpc.StatusCode.NOT_FOUND, "Order not found")
        except InvalidOrderState as e:
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, str(e))
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))


    def ShipOrder(self, request, context):
        try:
            order = self.service.ship_order(
                order_id = request.order_id
            )
            return order_pb2.ShipOrderResponse(
                order = self._to_proto(order)
            )
        except OrderNotFound:
            context.abort(grpc.StatusCode.NOT_FOUND, "Order not found")
        except InvalidOrderState as e:
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, str(e))
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))


    def CancelOrder(self, request, context):
        try:
            order = self.service.cancel_order(
                order_id = request.order_id,
                requester_id = request.requester_id,
                requester_role = request.requester_role,
            )
            return order_pb2.CancelOrderResponse(
                order = self._to_proto(order)
            )
        except OrderNotFound:
            context.abort(grpc.StatusCode.NOT_FOUND, "Order not found")
        except UnauthorizedOrderAction as e:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, str(e))
        except InvalidOrderState as e:
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, str(e))
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))
