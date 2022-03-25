import pandas as pd
from pathlib import Path
import sqlite3
from mysql.connector import Error

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    Path("./logistic.db").touch()
    con = sqlite3.connect("logistic.db")

    parse_dates = [
        'created_at',
        'in_transit_to_local_distribution_at',
        'local_distribution_at',
        'in_transit_to_deliver_at',
        'delivered_at',
        'delivery_estimate_date',
    ]

    data = pd.read_csv('logistic_case/logistics-case-v3.csv', parse_dates=parse_dates)
    data.to_sql("logistic", con, if_exists='append', index=False)



    print("end")
