#fruits = ["apple", "banana", "cherry"]
#if "banana" in fruits: # in is a membership operator that is used to check whether a value is present in a sequence or not.
#  print("Yes, 'banana' is in the fruits list")
#else:
#  print("No, 'banana' is not in the fruits list")

#fs = frozenset({"apple", "banana", "cherry"}) # frozenset() method is used to create an immutable (unchangeable) set.
#print(fs) # Output: frozenset({'apple', 'banana', 'cherry'})
#fs.add("orange") # This will raise an error
#print(fs) # Output: AttributeError: 'frozenset' object has no attribute 'add'


v = range(0,9) # range() function returns a sequence of numbers, starting from 0 by default, and increments by 1 (by default), and stops before a specified number.
for n in v: #for loop is used to iterate over a sequence (list, tuple, string) or other iterable objects.
  print(n) # Output: 0 1 2 3 4 5 6 7 8


car = {"brand": "Ford", "model": "Mustang", "year": 1964}

car.clear() # The clear() method removes all the elements from a dictionary.
print(car) # Output: {}


fruits = {"apple", "banana", "cherry", "Mango"}
for y in fruits:
    print(y)
    if y == "banana":
        break # The break statement is used to exit a loop when an condition is met.

for z in fruits:
   if z == "banana":
       break
   print(z) # Output: apple
   



#times table maker
num1 = int(input("Enter a number: "))
for x in range(1, 21):
    print(num1, 'x', x, '=', num1*x)