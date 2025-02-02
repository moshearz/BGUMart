from persistence import *
import sys

def main(args : list[str]):
    inputfilename : str = args[1]

    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")

            product_id = splittedline[0]
            quantity = int(splittedline[1]) # if negative == sale, if positive == supply
            activator_id = splittedline[2] #employee id (sales) or supplier id (supplies..) 
            date = splittedline[3]

            product = repo.products.find(id=product_id)[0]

            if quantity == 0:
                continue

            if quantity < 0 and product.quantity < -quantity:
                continue
            
            product.quantity += quantity
            repo.products.update(product)
            repo.activities.insert(Activitie(product_id, quantity, activator_id, date)) # Log the transaction in the database

if __name__ == '__main__':
    main(sys.argv)