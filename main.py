# Imports
import os
import argparse
import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import parse
from termcolor import colored
from tabulate import tabulate
from product import product
from functools import reduce 
from report import report
import markdown
from timemachine import time_machine

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.

parser = argparse.ArgumentParser()  # prog="SuperPy", description="Inventory management system")

input = parser.add_subparsers(dest="input")

buy = input.add_parser("buy", help="What would you like to buy?")

buy.add_argument("-i", "--item", type=str, required=True, help="Name of item (NO SPACES BETWEEN WORDS, use underscore instead)")
buy.add_argument("-a", "--amount", type=int, required=True, help="Amount to buy")
buy.add_argument("-c", "--cost", type=float, required=True, help="Cost of 1 piece of the item bought")
buy.add_argument("-pd", "--purchdate", type=lambda d: datetime.strptime(d, '%Y-%m-%d'), required=True, help="Expiration date of item in Year-month-day")
buy.add_argument("-expd", "--expdate", type=lambda d: datetime.strptime(d, '%Y-%m-%d'), required=True, help="Expiration date of item in Year-month-day")

# example: python main.py buy -i tomato -a 5 -c 3.23 -pd 2023-3-3 -expd 2024-11-22

sell = input.add_parser("sell", help="Sell products on stock")

sell.add_argument("-i", "--item", type=str, required=True, help="Name of item (NO SPACES BETWEEN WORDS, use underscore instead")
sell.add_argument("-a", "--amount", type=int, required=True, help="Amount to sell")
sell.add_argument("-p", "--price", type=float, required=True, help="Price of 1 piece at which the item is sold")
sell.add_argument("-sd", "--selldate", type=lambda d: datetime.strptime(d, '%Y-%m-%d'), required=True, help="Sell date of item in Year-month-day")

# example: python main.py sell -i tomato -a 8 -p 2.99 -sd 2023-3-30

reporting = input.add_parser("report", help="Reports for: Items on stock, amount on stock and P/L report over specified time period")

reporting.add_argument("-r", "--report", choices=["stock", "total_stock", "profit_loss", "profit_graph"], required=True, help="Stock per item, total stock of ALL items or P/L report over specified time period")
reporting.add_argument("-start", "--start_date", type=lambda d: datetime.strptime(d, '%Y-%m-%d'), help="Start date of P/L report")
reporting.add_argument("-end", "--end_date", type=lambda d: datetime.strptime(d, '%Y-%m-%d'), help="End date of P/L report")

# python main.py report -r total
# python main.py report -r total_stock
# python main.py report -r profit_loss -start 2023-3-3 -end 2023-5-12
# python main.py report profit_graph


timemachine = input.add_parser("time", help="The march of time is relentless")

timemachine.add_argument("--reset_all", choices=["reset_all"], required=False, help="WARNING: EVERYTHING IS RESET: Resets date to today. Inventory and sold are emptied. Only use on start up or when restarting")
timemachine.add_argument("-a", "--advance", type=int, help="Advance time by x (int) days")

# python main.py --reset_all reset all
# python main.py time -a 5

args = parser.parse_args()


if args.input == "buy":
    item = args.item
    amount = args.amount
    cost = args.cost
    purchdate = args.purchdate
    expdate = args.expdate
    product.buy(item, amount, cost, purchdate, expdate)

elif args.input == "sell":
    item = args.item
    amount = args.amount
    price = args.price
    selldate = args.selldate
    product.sell(item, amount, price, selldate)

elif args.input == "report":
    start_date = args.start_date
    end_date = args.end_date
    if args.report == "total_stock":
        report.total_stock()
    elif args.report == "profit_loss":
        start_date = args.start_date
        end_date = args.end_date
        report.profit_loss(start_date, end_date)
    elif args.report == "stock":
        report.stock()
    elif args.report == "profit_graph":
        report.profit_loss_graph()

elif args.input == "time":
    advance = args.advance
    if args.reset_all == "reset_all":
        time_machine.reset_all()
    elif isinstance(args.advance, int):
        time_machine.advance_time(advance)

