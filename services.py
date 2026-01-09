from db_models import Account, Transaction
from sqlalchemy import BigInteger, select
import logging
from fastapi import HTTPException

logging.basicConfig(
    level=logging.INFO,
    filename="services.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

handler = logging.FileHandler("services.log")
handler.setLevel(logging.WARNING)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def create_account(db, name: str, phone_no: BigInteger, address: str, age: int):
    try:
        acc_details = Account(
            name=name, phone_no=phone_no, address=address, age=age, balance=0.0
        )

        db.add(acc_details)
        db.commit()
        db.refresh(acc_details)

        return acc_details

    except Exception as e:
        logging.exception("Enter valid details for account creation, Error: ", e)


def deposit(db, id: int, amount: int):
    try:
        user_model = db.query(Account).filter(Account.id == id).first()
        user_id = user_model.id

        if not user_model.id:
            logging.warning("This ID is not exist for deposit, enter valid ID")
            raise HTTPException(
                status_code=404, detail="Account ID is not exist for deposit"
            )

        user_model.balance += amount

        stmt = Transaction(
            acc_id=user_id,
            balance_after=user_model.balance,
            amount=amount,
            description="DEPOSIT",
        )

        db.add(stmt)
        db.commit()
        db.refresh(stmt)

        return stmt

    except Exception as e:
        raise HTTPException(status_code=404, detail="Details are not valid")


def withdraw(db, id: int, amount: int):
    try:

        user_model = db.query(Account).filter(Account.id == id).first()
        user_id = user_model.id

        if not user_id:
            logging.warning("This ID is not exist for withdrawal, enter valid ID")
            raise HTTPException(
                status_code=404, detail="Account ID is not exist for withdrawal"
            )

        if amount > user_model.balance:
            logging.warning("Insufficient Balance for withdrawal")
            raise HTTPException(status_code=404, detail="Insufficient balance")

        user_model.balance -= amount

        stmt = Transaction(
            acc_id=user_id,
            balance_after=user_model.balance,
            amount=amount,
            description="WITHDRAWAL",
        )

        db.add(stmt)
        db.commit()
        db.refresh(stmt)

        return stmt

    except Exception as e:
        raise HTTPException(status_code=404, detail="Details are not valid")


def get_balance(db, id: int):
    try:
        user_model = db.query(Account).filter(Account.id == id).first()
        user_id = user_model.id

        if not user_id:
            logging.warning("This ID is not exist to check balance, enter valid ID")
            raise HTTPException(status_code=404, detail="Account ID is not exist")

        return user_model

    except Exception as e:
        raise HTTPException(status_code=404, detail="Details are not valid")


def get_account(db, id: int):
    try:
        user_model = db.query(Account).filter(Account.id == id).first()
        user_id = user_model.id

        if not user_id:
            logging.warning(
                "This ID is not exist to fetched account details, enter valid ID"
            )
            raise HTTPException(status_code=404, detail="Account ID is not exist")

        logging.info(f"Account {id} fetched successfully")

        return user_model

    except Exception as e:
        raise HTTPException(status_code=404, detail="Details are not valid")


def transaction_history(db, id: int):
    try:
        user_model = db.query(Account).filter(Account.id == id).first()
        user_id = user_model.id

        if not user_id:
            logging.warning(
                "This ID is not exist, enter valid ID to show transactoin history"
            )
            raise HTTPException(status_code=404, detail="Account ID is not exist")

        stmt = (
            select(Transaction)
            .where(Transaction.acc_id == id)
            .order_by(Transaction.updated_at.desc())
        )

        show = db.execute(stmt).scalars().all()

        return show

    except Exception as e:
        raise HTTPException(status_code=404, detail="Details are not valid")
