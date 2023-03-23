1. By using pandas i can filter the entire dataset before starting calculations
decreasing the resources required.

example:

df_sell = pd.read_csv("inventory.csv")
stocklist = df_sell.loc[(df_sell["Product"] == item) & (df_sell["Stock"] > 0), "Stock"].tolist()
Uidlist = df_sell.loc[(df_sell["Product"] == item) & (df_sell["Stock"] > 0), "UniqueID"].tolist()

When selling items I filter out the item to be sold and from there only the lines which actually have stock.
From here i create 2 list. 1 list containing the stock and 1 list containing the associated Unique ID. 
Continues @ point 2

The same is done when products spoil:
df_get_Uid = df_inventory.loc[df_inventory.index.isin(spoiled_items_list) & (df_inventory["Stock"] > 0)]

By checking expiration dates Unique IDs are put into a list. All items associated with this list are set to stock 0 and
the sold.csv file is updated. Technically these items are not sold but their "sell price" is 0.

2. With a for loop over these 2 lists (which always have the same lenght) a for loop with if/elif checks 
4 different possibilities. Since products of the same type might be split on expiration date (and thus have a seperate Uid and line in the csv file) the loop has to account for this. This is done by first checking if enough total stock is available and then going line by line to adjust stock until the total amount sold has been deduced from the inventory.
    1. if total < amount:       checks if total sold is more than stock available. Rejects transaction if True
    2. if amount == supply:     checks if total sold or amount left from previous calculations is equal to first instance of stock available. Makes changes to files and ends loop.
    3. elif amount < supply:    if amount sold or amount left from previous calculations is smaller than the first instance of inventory encountered it adjusts the inventory and ends the loop.
    4. elif amount > supply:    If the total amount sold or amount left from previous calculations is greater than the first supply encoutered by the loop the amount left to continue through the calculations is altered by the amount which was in cet data record, inventory is adjusted and the loop continues

Unfortunately this loop does not check expiration date. It was assumed that the oldest record always had the stock which is to expire first.

3. As an extra feature i thought of what would actually be usefull for someone using a program like this and i concluded that automatic backups are always a good thing. When the "advance time" command is used the program checks if it's the 1st of the month or if this day was skipped by the command. If so a backup is made in a seperate folder. If another month has passed the file is overwriten. Meaning the total data is updated.

