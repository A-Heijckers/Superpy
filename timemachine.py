import os
import pandas as pd
import numpy as np
from functools import reduce
import datetime
import datedelta
from product import product
from datetime import timedelta
from backup import backups

class time_machine():

    def __init__(self):
        pass

    def reset_all():
        cwd = os.getcwd()

        df_inventory = pd.DataFrame(columns=["UniqueID", "Product", "BuyPrice", "Stock", "BuyDate", "ExpirationDate"])
        df_inventory.to_csv('inventory.csv', index=False)

        df_sell = pd.DataFrame(columns=["UniqueID", "Product", "Amount", "BuyPrice", "SellPrice", "Profit", "SellDate"])
        df_sell.to_csv('sold.csv', index=False)

        def set_start_date():
            if not os.path.exists("time"):
                os.makedirs("time")
            time_path = os.path.join(cwd, "time")
            day_file = open(time_path + "\\day.txt", "w")
            day_file.write(str(datetime.datetime.now().date()))
            print(f'Todays date is {datetime.datetime.now().date()}')
        set_start_date()

    def set_date(date): 
        datestr = str(date) 
        datestr = datestr[0:10]     
        with open('time\\day.txt', "w") as time_file:
            time_file.write(datestr)
        print(f'Todays date is {datestr}')
        start_date = "1985-02-02"        
        end_date = str(datestr)
        product.perished_products(start_date, end_date)
    
    def advance_time(advance):
        with open('time\\day.txt') as time_file:
            current_date = time_file.readline()
        current_date = datetime.datetime.strptime(current_date, "%Y-%m-%d").date()
        start_delta = current_date

        start_date = str(current_date)
        current_date = current_date + (advance * datedelta.DAY)  
        end_delta = current_date
        current_date = str(current_date)
        end_date = current_date

        delta = (end_delta - start_delta)
        all_days = []
        for i in range(delta.days + 1):
            day = start_delta + timedelta(days=i)
            day = day.strftime('%Y-%m-%d')
            all_days.append(day)
        with open('time\\day.txt', "w") as time_file:
            time_file.writelines(current_date)
        print(f"Advanced time by {advance} days")
        print(f'Todays date is {current_date}')

        first_of_month = "-01"
        for x in all_days:
            if x[-3:] == first_of_month:
                backups.make_backups()
                print(f"Backups have been made of inventory.csv and sold.csv for all data up to {current_date}")
        product.perished_products(start_date, end_date)



