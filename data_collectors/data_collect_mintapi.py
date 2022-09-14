import mintapi
import pandas as pd
from data_collectors.authentication import username, password, token

def obtain_df():
    transactions = []

    mint = mintapi.Mint(
        username,
        password,
        mfa_method="soft-token",
        mfa_token=token,
        headless=True,
        session_path=None,
        driver=None
    )

    transactions_data = mint.get_transaction_data()

    for transaction in transactions_data:
        transactions.append({"date": transaction["date"], "description": transaction["description"], "category": transaction["category"]["name"], "amount": transaction["amount"]})
    
    transactions_df = pd.DataFrame(transactions)
    return transactions_df




    