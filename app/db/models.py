from datetime import datetime, timezone
from sqlalchemy import Integer, String, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


# funcion callable aware para default de created_at
def utc_now():
    return datetime.now(timezone.utc)


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    user_id: Mapped[int] = mapped_column(Integer, nullable = False)
    status: Mapped[str] = mapped_column(String(32), nullable = False)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone = True), default = utc_now, nullable = False)
