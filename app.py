import streamlit as st
from api_client import *
from ui_utils import show_api_error

st.set_page_config("Bank App", layout="wide")
st.title("🏦 Banking Management System")

tabs = st.tabs([
    "Create Account",
    "Deposit",
    "Withdraw",
    "Balance",
    "Account Details",
    "Transactions",
    "Update Account",
    "Delete Account"
])


with tabs[0]:
    st.header("Create Account")

    with st.form("create"):
        name = st.text_input("Name")
        phone = st.text_input("Phone No")
        address = st.text_input("Address")
        age = st.number_input("Age", min_value=1)
        submit = st.form_submit_button("Create")

        if submit:
            res = create_account({
                "name": name,
                "phone_no": phone,
                "address": address,
                "age": age
            })

            if res.ok:
                st.success("Account created")
                st.json(res.json())
            else:
                st.error(show_api_error(res))

with tabs[1]:
    st.header("Deposit Money")

    acc_id = st.number_input("Account ID", min_value=1)
    amount = st.number_input("Amount", min_value=1.0)

    if st.button("Deposit"):
        res = deposit({"id": acc_id, "amount": amount})

        if res.ok:
            st.success("Amount deposited")
            st.json(res.json())
        else:
            st.error(show_api_error(res))

with tabs[2]:
    st.header("Withdraw Money")

    acc_id = st.number_input("Account ID", min_value=1, key="w_id")
    amount = st.number_input("Amount", min_value=1.0, key="w_amt")

    if st.button("Withdraw"):
        res = withdraw({"id": acc_id, "amount": amount})

        if res.ok:
            st.success("Withdrawal successful")
            st.json(res.json())
        else:
            st.error(show_api_error(res))

with tabs[3]:
    st.header("Check Balance")

    acc_id = st.number_input("Account ID", min_value=1, key="b_id")

    if st.button("Get Balance"):
        res = get_balance(acc_id)

        if res.ok:
            st.metric("Balance", res.json()["balance"])
        else:
            st.error(show_api_error(res))

with tabs[4]:
    st.header("Account Details")

    acc_id = st.number_input("Account ID", min_value=1, key="a_id")

    if st.button("Show Account"):
        res = get_account(acc_id)

        if res.ok:
            st.json(res.json())
        else:
            st.error(show_api_error(res))

with tabs[5]:
    st.header("Transaction History")

    acc_id = st.number_input("Account ID", min_value=1, key="t_id")

    if st.button("Show Transactions"):
        res = transaction_history(acc_id)

        if res.ok:
            data = res.json()
            if isinstance(data, list):
                st.dataframe(data)
            else:
                st.json(data)
        else:
            st.error(show_api_error(res))

with tabs[6]:
    st.header("Update Account")

    acc_id = st.number_input("Account ID", min_value=1, key="u_id")
    name = st.text_input("Name")
    phone = st.text_input("Phone No")
    address = st.text_input("Address")
    age = st.number_input("Age", min_value=0)

    if st.button("Update"):
        params = {}

        if name.strip():
            params["name"] = name

        if phone.strip():
            params["phone_no"] = int(phone)

        if address.strip(): 
            params["address"] = address

        if age > 0:
            params["age"] = age

        res = update_account(acc_id, params)

        if res.ok:
            st.success("Account updated")
            st.json(res.json())
        else:
            st.error(show_api_error(res))

with tabs[7]:
    st.header("Delete Account")

    acc_id = st.number_input("Account ID", min_value=1, key="d_id")

    confirm = st.checkbox("Confirm delete")

    if st.button("Delete Account"):
        if not confirm:
            st.warning("Please confirm delete")
        else:
            res = delete_account(acc_id)

            if res.ok:
                st.success("✅ Account deleted successfully")
            else:
                st.error(show_api_error(res))
