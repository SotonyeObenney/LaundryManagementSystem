from ..extensions import db
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import mapped_column, Mapped

class Service(db.Model):
    __tablename__ = "service"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f"<Service {self.name}>"