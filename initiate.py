import sys
import os
from persistence import repo, Branche, Supplier, Product, Employee, Activitie

def add_branche(repo, splittedline: list[str]):
    repo.branches.insert(Branche(int(splittedline[0]), splittedline[1], int(splittedline[2])))

def add_supplier(repo, splittedline: list[str]):
    repo.suppliers.insert(Supplier(int(splittedline[0]), splittedline[1], splittedline[2]))

def add_product(repo, splittedline: list[str]):
    repo.products.insert(Product(int(splittedline[0]), splittedline[1], float(splittedline[2]), int(splittedline[3])))

def add_employee(repo, splittedline: list[str]):
    repo.employees.insert(Employee(int(splittedline[0]), splittedline[1], float(splittedline[2]), int(splittedline[3])))

adders = {
    "B": add_branche,
    "S": add_supplier,
    "P": add_product,
    "E": add_employee
}

def main(args: list[str]):
    inputfilename = args[1]

    # Close connection first and remove file if it exists
    repo._close()
    if os.path.isfile("bgumart.db"):
        try:
            os.remove("bgumart.db")
        except OSError:
            pass

    # Reinitialize the singleton repo and create tables
    repo.reinitialize()
    repo.create_tables()
    
    # Process input file
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline: list[str] = line.strip().split(",")
            adders.get(splittedline[0])(repo, splittedline[1:])

if __name__ == '__main__':
    main(sys.argv)