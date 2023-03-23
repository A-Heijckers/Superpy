import os
import argparse
import csv
import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import parse
from termcolor import colored
from tabulate import tabulate
from functools import reduce
import datedelta
import matplotlib.pyplot as plt


class report():

    def __init__(self, start_date=None, end_date=None):
        self.start_date = start_date
        self.end_date = end_date

    def stock():
        df_stock = pd.read_csv("inventory.csv")
        stocklist = df_stock.loc[(df_stock["Stock"] > 0)]    
        print(tabulate(stocklist, showindex=False, headers=["UniqueID", "Products", "BuyPrice", "Stock", "BuyDate", "ExpirationDate"]))
        stocklist.to_csv('stockreport.csv', index=False)

        

    def total_stock():
        df_total_stock = pd.read_csv("inventory.csv")
        productlist = df_total_stock["Product"].tolist()
        productlist = set(productlist)

        total_stock = {}
    
        for x in productlist:
            try:
                stocklist = df_total_stock.loc[(df_total_stock["Product"] == x) & (df_total_stock["Stock"] > 0), "Stock"].tolist()
                total = reduce(lambda x, y: x + y, stocklist)
                total_stock.update({x: total})
            except TypeError:
                continue           

        df_total_stock_report = pd.DataFrame.from_dict(total_stock, orient='index')
        df_total_stock_report.to_csv("totalstock.csv", index_label=["Products"], header=["Stock"])
        print(tabulate(df_total_stock_report, headers=["Products", "Stock"]))

    def profit_loss(start_date, end_date):
        df_PnL = pd.read_csv("sold.csv")
        sell_dates = df_PnL.loc[:, "SellDate"].tolist()
        start_date = start_date.date()
        end_date = end_date.date()
        delta = end_date - start_date
        
        all_days = []
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            day = day.strftime('%Y-%m-%d')
            all_days.append(day)
        
        profit_list = []
        for x in sell_dates:
            if x in all_days:
                profit_list.append(x)
        profit_list = list(set(profit_list))
        df_PnL.set_index("SellDate", inplace=True)
        total_profit = df_PnL.loc[profit_list, "Profit"].tolist()
        try:
            total_profit = round(reduce(lambda x, y: x + y, total_profit), 2)
     
            if total_profit < 0:
                print(f'Between {start_date} and {end_date} we\'ve \
made a total loss of {total_profit} and require immediate government bailouts')
            else:
                print(f'The total profit between {start_date} and {end_date} = {total_profit} euros')
        except TypeError:
            print("nothing sold yet")

    def profit_loss_graph():
        df_profit_plot = pd.read_csv("sold.csv")

        productlist = df_profit_plot["Product"].tolist()
        productlist = list(set(productlist))

        totals = []
        for x in productlist:
            profit = df_profit_plot.loc[(df_profit_plot["Product"] == x), "Profit"].tolist()
            total = reduce(lambda x, y: x + y, profit)
            totals.append(total)

        fig, ax = plt.subplots()
        ax.bar(productlist, totals)
        ax.set_ylabel('Total profit')
        ax.set_title('Profit per product')

        plt.show()
                



