from ..extensions import db
from sqlalchemy import String, Float
from sqlalchemy.orm import mapped_column, Mapped

class Service(db.Model):
    __tablename__ = "service"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_type: Mapped[str] = mapped_column(String(100), nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)

    def __repr__(self):
        return f"<Service {self.service_type}>"