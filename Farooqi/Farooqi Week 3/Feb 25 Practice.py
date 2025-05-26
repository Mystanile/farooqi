#1. Even or Odd Check
num1 = int(input("Enter a number: "))
if num1 % 2 == 0:
    print("The number is even.")
else:
    print("The number is odd.")
#2. Age-Based Eligibility Check (real world application)
num2 = int(input("Enter your age: "))
if num2 >= 18:
    print("You are eligible to vote.")
else:
    print("You are not eligible to vote.")
#3. Number comparison
num3 = int(input("Enter a number: "))
num4 = int(input("Enter another number: "))
if num3 > num4:
    print("The first number is greater.")
elif num3 < num4:
    print("The second number is greater.")
else:
    print("Both numbers are equal.")
#4. Leap Year Check
year = int(input("Enter a year: "))
if year % 4 == 0:
    if year % 100 == 0:
        if year % 400 == 0:
            print("The year is a leap year.")
        else:
            print("The year is not a leap year.")
    else:
        print("The year is a leap year.")
else:
    print("The year is not a leap year.")
#5. Positive, Negative or Zero Check
num5 = int(input("Enter a number: "))
if num5 > 0:
    print("The number is positive.")
elif num5 < 0:
    print("The number is negative.")
else:
    print("The number is zero.")