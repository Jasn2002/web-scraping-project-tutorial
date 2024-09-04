import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

def find_table_by_name(tables : list, name : str) -> int:
    index  : int = 0

    for table in tables:
        if name in str(table):
            return index - 1
        else: index += 1
    return index - 1 

def create_sql_database(data_frame : pd.DataFrame):
    connection = sqlite3.connect(s"New_Database.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS revenue (Date, Revenue)""")
    connection.commit()

    return data_frame.to_sql('revenue', connection, if_exists='append', index=False)
    

def custom_web_scraping(url : str) -> None:

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

    web_response = requests.get(url, headers=headers)

    if web_response.status_code != 200:
        print('Something went wrong! Status: ', web_response.status_code)
        return None
    
    html_data = web_response.text
    
    soup = BeautifulSoup(html_data,"html.parser")
    

    tables = soup.find_all('table')
    table_index = find_table_by_name(tables, "Tesla Quarterly Revenue")
    table_headers = ["Date", "Revenue"]
    
    
    rows = []
    for tr in tables[table_index].tbody.find_all("tr"):
        
        cells = [td.get_text().replace("$", "").replace(",", "").strip() for td in tr.find_all('td')]
        rows.append(cells)

     # Create DataFrame
    df = pd.DataFrame(rows, columns=table_headers)
    df.dropna()

    sql_db = create_sql_database(df)

    

custom_web_scraping(url)


