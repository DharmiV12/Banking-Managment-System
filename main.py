from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session 
from database import engine, SessionLocal
from db_models import Base, Account, Transaction
from services import *
from model import AccountResponse, CreateAccount, AccountRequest,BalanceResponse, ShowBalance, UpdateResponse
import logging

logging.basicConfig(level=logging.INFO, filename='services.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

handler = logging.FileHandler('services.log')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create-account/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def add_account(acc:CreateAccount, db:Session = Depends(get_db)):
    logging.info("Add Account")
    
    if db.query(Account).filter(Account.phone_no == acc.phone_no).first():
        logging.warning("Add different phone number")
        raise HTTPException(status_code=404, detail="Phone no is not valid")
    
    account = create_account(db, acc.name, acc.phone_no, acc.address, acc.age)

    logging.info("Account created")

    return account


@app.post("/deposite/", response_model=BalanceResponse, status_code=status.HTTP_200_OK)
def deposite_money(acc:AccountRequest, db:Session = Depends(get_db)):
    logging.info("Deposit")
    
    account = deposit(db, acc.id, acc.amount)

    #logging.info("Amount deposited")
    
    return account
    

@app.post("/withdrawal/", response_model=BalanceResponse)
def withdraw_money(acc:AccountRequest,  db:Session = Depends(get_db)):

    logging.info("Withdrawal")

    account = withdraw(db, acc.id, acc.amount)

    #logging.info("Amount withdraw successfully")
    
    return account


@app.get("/get-balance/{account_id}", response_model=ShowBalance)
def show_balance(account_id:int, db:Session = Depends(get_db)):

    logging.info("Show Balance")

    account = get_balance(db, account_id)

    #logging.info("Balance showed")
    
    return account


@app.get("/get-account/{account_id}", response_model=AccountResponse)
def show_account(account_id:int, db:Session = Depends(get_db)):

    logging.info("Account Details")

    account = get_account(db, account_id)

    #logging.info("Account details showed")
    
    return account


@app.get("/transaction-history/{account_id}")
def transactions(account_id:int, db:Session = Depends(get_db)):

    logging.info("Transaction History")

    account = transaction_history(db, account_id)

    #logging.info("Transaction hisory showed")

    return account


@app.put("/update-account/{account_id}", response_model=UpdateResponse)
def update_data(account_id:int, age:int =0, phone_no:int = 0, name:str="", address:str="", db:Session = Depends(get_db)):

    logging.info("Update Data")

    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        logging.warning("Account ID is not valid")
        raise HTTPException(status_code=404, detail="Account ID is not valid")
        
    if name:
        account.name = name
    if phone_no:
        account.phone_no = phone_no
    if address:
        account.address = address
    if age:
        account.age = age

    db.commit()
    db.refresh(account)

    #logging.info("Data Updated")

    return account


@app.delete("/delete-account/{account_id}")
def delete_account(account_id:int, db:Session = Depends(get_db)):
 
    logging.info("Account delete")
    
    history = db.query(Transaction).filter(Transaction.acc_id == account_id).all()

    if not history:
        logging.warning("History for that account id is not found")
        raise HTTPException(status_code=404, detail="Account history is not found")

    for history in history:
        db.delete(history)

    db.commit()

    #logging.info("Transaction history deleted")
    
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        logging.warning("Account id is not found")
        raise HTTPException(status_code=404, detail="Account ID is not found")
    
    db.delete(account)
    db.commit()

    #logging.info("Account deleted")
    
    return {
    "message": "Account deleted successfully",
    "account_id": account_id
}
