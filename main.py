import streamlit as st
import pandas as pd
import numpy as np
from data_collectors.data_collect_from_csv import CleanData
import matplotlib.pyplot as plt
import july
from july.utils import date_range
from data_collectors.data_collect_mintapi import obtain_df

# Establish July framework dates
dates = date_range("2022-03-28", "2022-06-28")

TRANSACTIONS = "./csv_data/transactions.csv"

# CSS to inject contained in a string
hide_table_row_index = """
        <style>
        thead tr th:first-child {display:none}
        tbody th {display:none}
        </style>
        """

def main():
    plot_with_mintapi()

def plot_with_csv():
    '''Takes in downloaded CSV as in=`put'''
    st.title("Transaction Data Analyzer")

    # Initialize object
    clean_data = CleanData(TRANSACTIONS)
    data = clean_data.load_data()

    graphical_analysis(clean_data, data)

def plot_with_mintapi():
    st.title("Transaction Data Analyzer")

    data = CleanData(obtain_df())

    graphical_analysis(data, data.transactions)


def graphical_analysis(obj, data):

    # Net Income
    profit = obj.spenditure(data)
    income = profit["Net Income"]
    st.metric("Net Income", round(income, 2), delta=None)

    # Total Spending
    spent = profit["Total Spent"]
    st.metric("Total Spent", round(spent, 2), delta=None)

    # Total Earned
    earned = profit["Total Made"]
    st.metric("Total Made", round(earned, 2), delta=None)

    # Spending by category
    st.subheader('Category')
    category_data = obj.category(data)
    fig, ax = plt.subplots(figsize=(10,13))
    ax.barh(category_data["category"], category_data["amount"])
    st.pyplot(fig)

    # Top 10 Largest Expenses
    st.subheader('Top 15 Largest Expenses')
    top_expenses = obj.largest_expenses(data)
    st.markdown(hide_table_row_index, unsafe_allow_html=True)    
    st.table(top_expenses.style.format({"Amount": "{:.2f}"}))

    # Calendar heatmap of spending
    date_frequency_dict = obj.frequency(data)
    july.heatmap(dates=dates, 
                data=date_frequency_dict, 
                cmap='github',
                month_grid=True, 
                horizontal=True,
                value_label=True,
                date_label=False,
                weekday_label=True,
                month_label=True, 
                year_label=False,
                colorbar=True,
                fontfamily="monospace",
                fontsize=12,
                title="Spending Calendar",
                titlesize='large',
                dpi=100)
    st.pyplot(plt) 


if __name__ == "__main__":
    main()