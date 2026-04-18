# Order Service

Microservicio que gestiona ordenes con DB propia y se expone via gRPC
(requester viene de otro microservicio a traves de api gateway autenticado)

- para que corran los tests de dominio hay que crear pytest.ini con la raiz
- grpc son casos de uso no CRUD
- arquitectura hexagonal, busca aislar la logica de negocio de elementos externos como BD, interfaces, apis, testea
  de forma aislada con mocks (tests de dominio), asi como en user-service y api-gateway
- DDD, diseño orientado al dominio (domain driven design)
- la ruta app/grpc no debe contener __init__.py porque python trata de importar la libreria oficial (cambiar nombre)
- la configuracion de alembic.ini y env.py hace que no lea la url desde .ini sino desde os.environ('DATABASE_URL')
- correr el servicio localmente con python

- python -m grpc_tools.protoc \
  -I app/rpc/proto \
  --python_out=app/rpc \
  --grpc_python_out=app/rpc \
  app/rpc/proto/order.proto
  (generar stubs en directorio)
- alembic init alembic
- alembic current
- alembic revision --autogenerate -m "create orders table"
- alembic upgrade head
- python -m app.rpc.server
- 