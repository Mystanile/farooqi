products = (("Apple", 1.50),("Banana", 0.75),("Orange", 1.25),("Mango", 2.00),("Grapes", 2.50))
product_name = input("Enter the product name: ")
found = False
for product in products:
    if product[0].lower() == product_name.lower():
        print(f"The price of {product[0]} is ${product[1]:.2f}") #.2f is used to print 2 decimal places
        found = True
        break
if not found:
    print("Product not found.")