from ..extensions import db
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime, timezone

class Delivery(db.Model):
    __tablename__ = "delivery"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), nullable=False, unique=True)
    delivery_address: Mapped[str] = mapped_column(String(200), nullable=False)
    delivery_type: Mapped[str] = mapped_column(String(20), nullable=False, default="delivery")
    delivery_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")

    order = relationship("Order", backref="delivery")

    def __repr__(self):
        return f"<Delivery {self.id} - {self.status}>"