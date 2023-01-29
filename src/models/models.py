import uuid

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.db import base


class Menu(base):
    """Модель меню."""

    __tablename__ = "menus"

    id = Column(
        UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    submenus = relationship(
        "Submenu", back_populates="menu", cascade="all, delete"
    )


class Submenu(base):
    """Модель подменю."""

    __tablename__ = "submenus"

    id = Column(
        UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(
        UUID, ForeignKey("menus.id", ondelete="CASCADE"), nullable=False
    )

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship(
        "Dish", back_populates="submenu", cascade="all, delete"
    )


class Dish(base):
    """Модель блюда."""

    __tablename__ = "dishes"

    id = Column(
        UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    submenu_id = Column(
        UUID, ForeignKey("submenus.id", ondelete="CASCADE"), nullable=False
    )

    submenu = relationship("Submenu", back_populates="dishes")
