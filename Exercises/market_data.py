# Start by importing the libraries. I like to use yfinance to get stock data.
# I use SQLite as a database you can store on your computer. It’s an efficient file-based database which makes it perfect for building research tools.
# It uses standard SQL so you can easily move to a different database like MySQL or Postgres.

from sys import argv

import pandas as pd
import yfinance as yf
import sqlite3

#Download and store stock price data.
# The script you are building will do two things:
#     Save data within a date range
#     Save data for the last trading day
# 
# To make it easy, create three functions to download the data, save data within a range, and save data for the last trading day.

# create a function to download the data with type hints
# type hints are a way to annotate your code so that you can tell what type of data a function should accept and return.

def get_market_data(ticker: str,start_date: str,end_date: str) -> pd.DataFrame:
    """
    Downloads data from Yahoo Finance
    """
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    #rename columns with lower case and replace spaces with underscores
    data.columns = [str(x).lower().replace(' ', '_') for x in data.columns]
    #adds the ticker column
    data['ticker'] = ticker
    return data

# create a function that uses get_market_data to get time series data and saves it into a database
# The function uses pandas to_sql method to save the data to a database.
def save_market_data(ticker: str, start_date: str, end_date: str, conn: sqlite3.Connection) -> None:
    """
    Saves stock data to database
    """
    data = get_market_data(ticker, start_date, end_date)
    data.to_sql(
        'yf_data', 
        conn, 
        if_exists='append', 
        index=False
    )
    return None
# create a function that saves the last trading day’s data into the database.
# The function grabs data from today and inserts it into the database.

def save_market_data_for_last_trading_day(ticker: str, conn: sqlite3.Connection) -> None:
    """
    Saves last trading day's data to database
    """
    today = pd.Timestamp.today()
    data = get_market_data(ticker, today, today)
    data.to_sql(
        'yf_data', 
        conn,
        # if_exists='append' means that if the table already exists, the data will be appended to it.
        if_exists='append',
            index=False
    )
    return None

# create a main function that will run the script
def main(ticker: str, start_date: str, end_date: str) -> None:
    # usage example for bulk insert
    #     python market_data.py bulk SPY 2022-01-01 2022-10-20
    # usage example for last session
    #     python market_aata.py last SPY

    # create a connection to the database
    conn = sqlite3.connect('market_data.sqlite')

    # if the user selects bulk, run the save_market_data function
    if argv[1] == 'bulk':
        save_market_data(ticker, start_date, end_date, conn)
        print(f"{symbol} saved between {start} and {end}")
    # if the user selects last, run the save_market_data_for_last_trading_day function
    elif argv[1] == 'last':
        save_market_data_for_last_trading_day(ticker, conn)
    # if the user selects anything else, print an error
    else:
        print('Usage: python market_data.py bulk <ticker> <start_date> <end_date>')
        print('Usage: python market_data.py last <ticker>')
    # close the connection to the database
    conn.close()
    return None

# create a command that runs the script from the command line

if __name__ == '__main__':
    # usage example for bulk insert
    #     python market_data.py bulk SPY 2022-01-01 2022-10-20
    # usage example for last session
    #     python market_aata.py last SPY

    # create a connection to the database
    conn = sqlite3.connect('market_data.sqlite')

    # if the user selects bulk, run the save_market_data function
    if argv[1] == 'bulk':
         ticker = argv[2]
         start_date = argv[3]
         end_date = argv[4]
         save_market_data(ticker, start_date, end_date, conn)
         print(f"{ticker} saved between {start_date} and {end_date}")
    # if the user selects last, run the save_market_data_for_last_trading_day function
    elif argv[1] == 'last':
         ticker = argv[2]
         save_market_data_for_last_trading_day(ticker, conn)
    # if the user selects anything else, print an error
    else:
         print('Usage: python market_data.py bulk <ticker> <start_date> <end_date>')
         print('Usage: python market_data.py last <ticker>')
    # close the connection to the database
    conn.close()
