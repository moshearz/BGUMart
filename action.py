from hmac import new
from math import prod
from persistence import *
import sys

def main(args : list[str]):
    inputfilename : str = args[1] #example: "actions.txt"

    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")
            #TODO: apply the action (and insert to the table) if possible

            product_id = splittedline[0]
            quantity = int(splittedline[1]) # if negative == sale, if positive == supply
            activator_id = splittedline[2] #employee id (sales) or supplier id (supplies..) 
            date = splittedline[3]

            product = repo.products.find(id=product_id) # repo.products Accesses the "products" table and then finds the product with the given id
            if not product: # if product is not found
                continue
            product = product[0]

            if quantity == 0:
                continue

            if quantity < 0: # sale
                employee = repo.employees.find(id=activator_id)
                if not employee or product.quantity < abs(quantity): # if employee is not found or the quantity is not enough
                    continue                
            else: # quantity >0 so its supply
                supplier = repo.suppliers.find(id=activator_id)
                if not supplier:
                    continue
            
            new_quantity = product.quantity + quantity
            repo.products.update({"quantity": new_quantity}, id=product_id)
            repo.activities.insert(Activity(product_id, quantity, activator_id, date)) # Log the transaction in the database


            

if __name__ == '__main__':
    main(sys.argv)