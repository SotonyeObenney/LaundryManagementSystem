from ..extensions import db
from sqlalchemy import String, Float, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

class OrderItem(db.Model):
    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"), nullable=False)
    item_type: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    service = relationship("Service")

    def calculate_cost(self):
        return self.quantity * self.price

    def __repr__(self):
        return f"<OrderItem {self.item_type} x{self.quantity}>"