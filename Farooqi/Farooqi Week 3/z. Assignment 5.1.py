input_list = input("Enter a list of numbers separated by spaces: ")
numbers = [int(number) for number in input_list.split()]
even_numbers = []
odd_numbers = []
for number in numbers:
    if number % 2 == 0:
        even_numbers.append(number)
    else:
        odd_numbers.append(number)
print(f"Even numbers: {even_numbers}")
print(f"Odd numbers: {odd_numbers}")
