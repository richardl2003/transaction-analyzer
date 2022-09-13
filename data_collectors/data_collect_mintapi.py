import mintapi
import pandas as pd
from authentication import username, password, token

def main():
    data = obtain_df()

def obtain_df():
    transactions = []

    mint = mintapi.Mint(
        username,
        password,
        mfa_method="soft-token",
        mfa_token=token,
        headless=False,
        session_path=None,
        driver=None
    )

    transactions_data = mint.get_transaction_data()

    for transaction in transactions_data:
        transactions.append({"date": transaction["date"], "description": transaction["description"], "category": transaction["category"]["name"], "amount": transaction["amount"]})
    
    transactions_df = pd.DataFrame(transactions)
    return transactions_df
    


if __name__ == "__main__":
    main()