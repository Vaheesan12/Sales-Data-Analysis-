import csv
from io import StringIO

CSV_DATA = """Order_ID,Order_Date,Customer_Name,Category,Product,Region,Quantity,Unit_Price,Discount,Sales,Profit
ORD001,2025-01-05,Amit Kumar,Electronics,Laptop,North,2,55000,0.05,104500,12000
ORD002,2025-01-08,Neha Sharma,Furniture,Chair,South,5,4000,0.10,18000,3500
ORD003,2025-01-15,Ravi Singh,Electronics,Mobile Phone,West,3,25000,0.02,73500,9000
ORD004,2025-02-03,Priya Das,Office Supplies,Printer,East,2,18000,0.05,34200,5000
ORD005,2025-02-12,Anil Verma,Furniture,Table,North,1,12000,0.00,12000,2500
ORD006,2025-03-02,Sunita Rao,Electronics,Tablet,South,4,22000,0.08,80960,11000
ORD007,2025-03-18,Mohit Jain,Office Supplies,Notebook,West,20,250,0.00,5000,1000
ORD008,2025-04-06,Kavita Roy,Furniture,Sofa,East,1,35000,0.15,29750,4500
"""

rows = list(csv.DictReader(StringIO(CSV_DATA)))

if __name__ == "__main__":
    print(rows)
