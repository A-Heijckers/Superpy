import sys
import os
import pandas as pd
import numpy as np
from functools import reduce
import datetime
import datedelta
from datetime import timedelta


class product():

    def __init__(self, item, amount, purchdate=None, expdate=None, cost=None, price=None, selldate=None):   # Maak speler aan
        self.item = item
        self.amount = amount
        self.expdate = expdate
        self.purchdate = purchdate
        self.cost = cost
        self.price = price
        self.selldate = selldate

    def buy(item, amount, cost, purchdate, expdate):
        df_buy = pd.read_csv("inventory.csv")

        def Uid():
            try:
                new_id = max(df_buy["UniqueID"].tolist()) + 1
                return new_id
            except ValueError:
                new_id = 1
                return new_id
        new_id = Uid()

        products = [new_id, item, cost, amount, purchdate, expdate]
        products = pd.DataFrame([products])
        products.to_csv('inventory.csv', mode='a', date_format='%Y-%m-%d', index=False, header=False)
        total_price = round((amount * cost), 2)
        
        print(f'You have bought {amount}x {item} for total of €{total_price} and €{cost} a piece')

    def sell(item, amount, price, selldate):
        df_sell = pd.read_csv("inventory.csv")
        stocklist = df_sell.loc[(df_sell["Product"] == item) & (df_sell["Stock"] > 0), "Stock"].tolist()
        Uidlist = df_sell.loc[(df_sell["Product"] == item) & (df_sell["Stock"] > 0), "UniqueID"].tolist()

        sales = amount

        def total_stock():
            try:
                total = reduce(lambda x, y: x + y, stocklist)
                return total
            except TypeError:
                print("Out of stock")
                sys.exit(1)
                
        total = total_stock()
        
        df_sell.set_index("UniqueID", inplace=True)

        for supply, Uid in zip(stocklist, Uidlist):
            if total < amount:
                print(f"We only have {total} unit(s) on stock")
                sys.exit(1)
            if amount == supply:
                cost = df_sell.at[Uid, "BuyPrice"]
                profit = (price - cost)
                profit = round(profit, 2)*amount
                products = [Uid, item, amount, cost, price, profit, selldate]
                products = pd.DataFrame([products])
                products.to_csv('sold.csv', mode='a', date_format='%Y-%m-%d', index=False, header=False)
                df_sell.at[Uid, "Stock"] = 0
                amount = 0
                break
            elif amount < supply:
                cost = df_sell.at[Uid, "BuyPrice"]
                profit = (price - cost)
                profit = round(profit, 2)*amount
                products = [Uid, item, amount, cost, price, profit, selldate]
                products = pd.DataFrame([products])
                products.to_csv('sold.csv', mode='a', date_format='%Y-%m-%d', index=False, header=False)
                df_sell.at[Uid, "Stock"] = supply - amount
                break
            elif amount > supply:
                cost = df_sell.at[Uid, "BuyPrice"]
                profit = (price - cost)
                profit = round(profit, 2)*supply
                products = [Uid, item, supply, cost, price, profit, selldate]
                products = pd.DataFrame([products])
                products.to_csv('sold.csv', mode='a', date_format='%Y-%m-%d', index=False, header=False)
                df_sell.at[Uid, "Stock"] = 0
                amount = amount - supply
                continue

        total_price = round((sales * price), 2)
        print(f'You have sold {sales}x {item} for total of €{total_price} and €{price} a piece')

        df_sell.reset_index(inplace=True)

        cwd = os.getcwd()
        file_stock = "inventory.csv"
        filename_stock = os.path.join(cwd, file_stock)

        open(filename_stock, 'a+', newline='')
        df_sell.to_csv(file_stock, index=False)  

    def perished_products(start_date, end_date):
        df_inventory = pd.read_csv("inventory.csv")
       
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        delta = (end_date - start_date)

        all_days = []
        for i in range(delta.days):
            day = start_date + timedelta(days=i)
            day = day.strftime('%Y-%m-%d')
            all_days.append(day)

        expiration_dates = df_inventory.loc[:, "ExpirationDate"].tolist()
        spoiled_items_list = []
        for x in expiration_dates:
            if x in all_days:
                spoiled_items_list.append(x)
        spoiled_items_list = list(set(spoiled_items_list))

        df_get_Uid = df_inventory.set_index("ExpirationDate", inplace=True)
        df_get_Uid = df_inventory.loc[df_inventory.index.isin(spoiled_items_list) & (df_inventory["Stock"] > 0)]
        Uid_list = df_get_Uid["UniqueID"].tolist()

        df_perish = pd.read_csv("inventory.csv")
        df_perish.set_index("UniqueID", inplace=True)
        for x in Uid_list:
            UniqueID = x
            product = df_perish.at[x, "Product"]
            buy_price = df_perish.at[x, "BuyPrice"]
            amount = df_perish.at[x, "Stock"]
            losses = round((buy_price * amount), 2)
            sell_price = 0
            profit = (amount * buy_price) * -1
            Sell_date = str(datetime.datetime.now().date())
            print(f"{amount}x {product} are past expiration date and have perished. We lost €{losses} in the process")
            products = [UniqueID, product, amount, buy_price, sell_price, profit, Sell_date]
            products = pd.DataFrame([products])
            products.to_csv('sold.csv', mode='a', date_format='%Y-%m-%d', index=False, header=False)
            df_perish.at[x, "Stock"] = 0
            
        df_perish.reset_index(inplace=True)
        cwd = os.getcwd()
        file_stock = "inventory.csv"
        filename_stock = os.path.join(cwd, file_stock)
        
        open(filename_stock, 'a+', newline='')
        df_perish.to_csv(file_stock, index=False)  
