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
import shutil

class backups():
    
    def make_backups():
        try:
            cwd = os.getcwd()
            if not os.path.exists("backups"):
                os.makedirs("backups")
            backup_path = os.path.join(cwd, "backups")
            inventory_file = "inventory.csv"
            sold_file = "sold.csv"
            shutil.copy(inventory_file, backup_path, follow_symlinks=True)
            shutil.copy(sold_file, backup_path, follow_symlinks=True)
        except FileNotFoundError:
            pass

    make_backups()


