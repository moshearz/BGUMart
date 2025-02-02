import os
from persistence import repo

def main():        
    print("Activities")
    activities = repo.activities.find_all()
    for row in activities:
        print(row)
    
    print("Branches")
    branches = repo.branches.find_all()
    for row in branches:
        print(row)
    
    print("Employees")
    employees = repo.employees.find_all()
    for row in employees:
        print(row)
    
    print("Products")
    products = repo.products.find_all()
    for row in products:
        print(row)
    
    print("Suppliers")
    suppliers = repo.suppliers.find_all()
    for row in suppliers:
        print(row)
    
    print("Employees report")
    employees_report = repo.execute_command("""
        SELECT e.name, e.salary, b.location, 
               IFNULL(SUM(CASE WHEN a.quantity < 0 THEN -a.quantity * p.price ELSE 0 END), 0) as total_sales_income
        FROM employees e
        JOIN branches b ON e.branche = b.id
        LEFT JOIN activities a ON e.id = a.activator_id
        LEFT JOIN products p ON a.product_id = p.id
        GROUP BY e.id
        ORDER BY e.name
    """)
    for row in employees_report:
        print(" ".join(map(str, row)))
    
    print("Activities report")
    activities_report = repo.execute_command("""
        SELECT a.date, p.description, a.quantity, 
               CASE WHEN a.quantity < 0 THEN e.name ELSE NULL END as seller_name,
               CASE WHEN a.quantity > 0 THEN s.name ELSE NULL END as supplier_name
        FROM activities a
        LEFT JOIN products p ON a.product_id = p.id
        LEFT JOIN employees e ON a.activator_id = e.id
        LEFT JOIN suppliers s ON a.activator_id = s.id
        ORDER BY a.date
    """)
    for row in activities_report:
        print(row)

if __name__ == '__main__':
    main()