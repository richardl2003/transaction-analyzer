import pandas as pd
import numpy as np
from july.utils import date_range

class CleanData:

    def __init__(self, transactions):
        self.transactions = transactions
    
    def load_data(self):
        '''Loaded the csv file into a pandas df'''
        data = pd.read_csv(self.transactions)
        data.rename(lambda x: str(x).lower(), axis="columns", inplace=True)
        del(data["labels"])
        del(data["notes"])

        # Add in positive and negative values to the amount column
        data["amount"] = np.where(data["transaction type"] == "debit", data["amount"]*(-1), data["amount"])
        data["date"] = pd.to_datetime(data["date"]).astype(str)
        
        return data
        
    def category(self, loaded_df):
        '''Gathers the amount spent per category'''
        category_df = loaded_df.groupby(["category"])["amount"].sum().reset_index()
        get_spending = category_df[category_df["amount"] < 0].sort_values(by="amount", ascending=False).reset_index(drop=True)
        get_spending["amount"] = get_spending["amount"] * (-1)
        return get_spending
    
    def largest_expenses(self, loaded_df):
        '''Filters for the 15 largest expenses'''
        top_df = loaded_df[['date', 'amount', 'description']].sort_values(by="amount", ascending=False).head(10).reset_index(drop=True)
        top_df.rename(lambda x: str(x).capitalize(), axis="columns", inplace=True)
        return top_df
    
    def spenditure(self, loaded_df):
        '''Calculates the net income'''
        net_income = loaded_df["amount"].sum()
        total_spent = loaded_df[loaded_df["amount"] < 0]["amount"].sum()
        total_made = loaded_df[loaded_df["amount"] > 0]["amount"].sum()

        return {"Net Income": net_income, "Total Spent": total_spent, "Total Made": total_made}
    
    def frequency(self, loaded_data):
        '''Creates a new dictionary based on purchases per day'''
        range_of_dates =  date_range("2022-03-28", "2022-06-28")
        range_of_dates = [date.strftime("%Y-%m-%d") for date in range_of_dates]

        spent_money_dates = loaded_data["date"].tolist()
        missing_dates = []

        for date in range_of_dates:
            if date not in spent_money_dates:
                missing_dates.append(date)

        day_frequency = loaded_data["date"].value_counts().sort_index()
        missing_series = pd.Series([0 for i in range(len(missing_dates))], index=missing_dates)
        combined = day_frequency.add(missing_series, fill_value=0)

        return combined.to_numpy().astype(int)

