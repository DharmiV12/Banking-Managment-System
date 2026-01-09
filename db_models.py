from database import engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Column, DateTime, Integer, Float, BigInteger
from datetime import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class TimeStemp(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Account(TimeStemp, Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone_no: Mapped[BigInteger] = mapped_column(
        BigInteger, unique=True, nullable=False
    )
    address: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    balance: Mapped[float] = mapped_column(Float)
    transaction: Mapped[MutableList["Transaction"]] = relationship(
        "Transaction",
        back_populates="account",
        cascade="all,delete",
        passive_deletes=True,
    )


class Transaction(TimeStemp, Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    acc_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    balance_after: Mapped[int] = mapped_column(Float)
    amount: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String)
    account: Mapped[MutableList["Account"]] = relationship(
        "Account", back_populates="transaction"
    )
