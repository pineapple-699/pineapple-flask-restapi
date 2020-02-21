import csv
from models.inventory import InventoryModel


data = open("pineapple_inventory.csv", "r")
content = csv.reader(data)
inventory = []

print(type(content))
# for inst in content:
    # inventory.append(InventoryModel(inst))

