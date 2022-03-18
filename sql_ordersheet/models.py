from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DATETIME, Float
from sqlalchemy.orm import relationship

from .database import Base


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    hashId = Column(String)
    price = Column(Float)
    active = Column(Boolean, default=True)

    #Items = relationship("items", back_populates="order_sheets")


class OrderSheet(Base):
    __tablename__ = "order_sheets"

    id = Column(Integer, primary_key=True, index=True)
    hash_order_id = Column(String)  # para agrupar pedidos
    #item = Column(Integer, ForeignKey("items.id"))
    item = Column(Integer)
    consumed = Column(Boolean, default=False)
    consumed_location = Column(String, default="None")

    # @TODO: ajusutar o formato d e datetime para um valor padrão
    consumed_time = Column(String, default="")

    #order_sheets = relationship("order_sheets", back_populates="items")
