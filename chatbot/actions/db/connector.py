import json

class restaurant_db:
    def __init__(self, restaurant_db):
        with open(restaurant_db, 'r') as f:
            self.restaurant_db = json.load(f)
    
    def get_restaurant_by_id(self, id):
        return self.restaurant_db[id]
    
    def get_restaurant_by_name(self, name):
        for restaurant in self.restaurant_db:
            if restaurant['restaurant_name'] == name:
                return restaurant
        return None
    
    def get_restaurant_adress(self, id):
        return self.restaurant_db[id]['restaurant_address']
    
    def get_restaurant_phone(self, id):
        return self.restaurant_db[id]['restaurant_phone']
    
class inventory_db:
    def __init__(self, inventory_db):
        with open(inventory_db, 'r') as f:
            self.inventory_db = json.load(f)
    
    def get_item_by_id(self, id):
        return self.inventory_db[id]
    def get_item_id_by_name(self, name):
        for item in self.inventory_db:
            if self.inventory_db[item]["product_name"] == name:
                return item
        return None
    def get_item_by_name(self, name): #fixed
        for item in self.inventory_db:
            if self.inventory_db[item]["product_name"] == name:
                return self.inventory_db[item]
        return None
    
    def get_item_quantity(self, item_id):
        return self.inventory_db[item_id]['quantity']
    
    def get_item_category(self, item_id):
        return self.inventory_db[item_id]['product_category']
    
    def get_restaurant_inventory(self, restaurant_id):
        inventory = []
        for item_id in self.inventory_db:
            if self.inventory_db[item_id]['restaurant_id'] == restaurant_id:
                print(self.inventory_db[item_id]['restaurant_id'])
                inventory.append(self.inventory_db[item_id])
        return inventory

class inventory_catalog:
    def __init__(self, inventory_catalog, inventory_db):
        with open(inventory_catalog, 'r') as f:
            self.inventory_catalog = json.load(f)
            self.inventory_db = inventory_db #used to get the name of the items
    
    def get_item_by_id(self, id):
        return self.inventory_catalog[id]
    
    def get_item_name(self, id):
        return self.inventory_db.get_item_by_id(id)['product_name'] # can be deleted
        
    
    def get_item_clicks(self, item_id):
        return self.inventory_catalog[item_id]['clicks_number']
    
    def get_item_proposed(self, item_id):
        return self.inventory_catalog[item_id]['proposed_number']
    
    def add_item_clicks(self, item_id, clicks):
        self.inventory_catalog[item_id]['clicks_number'] += clicks
        
    def add_item_proposed(self, item_id, proposed):
        self.inventory_catalog[item_id]['proposed_number'] += proposed
    
    def get_restaurant_inventory(self, restaurant_id): # can be deleted
        inventory = []
        for item_id in self.inventory_catalog:
            if self.inventory_catalog[item_id]['restaurant_id'] == restaurant_id:
                print(self.inventory_catalog[item_id]['restaurant_id'])
                inventory.append(self.inventory_catalog[item_id])
        return inventory
    
    def write_catalog(self, file): # write the catalog to json with name "file"
        with open(file, 'w') as f:
            json.dump(self.inventory_catalog, f)

""" rest_db = restaurant_db('./restaurants.json')
inv_db = inventory_db('./inventory.json')

address = rest_db.get_restaurant_adress(id='1')  # Get the address of the first restaurant
first_restaurant = rest_db.get_restaurant_by_id(id='1')  # Get the first restaurant

first_rest_inventory = inv_db.get_restaurant_inventory(restaurant_id=1) # Get the inventory of the first restaurant
item_quantity = inv_db.get_item_quantity(item_id='1')  # Get the quantity of the first item
print(first_rest_inventory) 

inv_db = inventory_db('./inventory.json')
catalog = inventory_catalog('./inventory_catalog.json', inv_db)
print(catalog.get_item_name('1')) 
"""