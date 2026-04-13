from app.extensions import db
from flask_login import UserMixin
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column
    # phone
    # address
    # passwo
    # rol
    # created