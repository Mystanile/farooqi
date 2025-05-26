char_tuple = (input("Enter some characters: "))
char_tuple = tuple(char_tuple)
print(f"You inputted {char_tuple}")
vowels = 'aeiouAEIOU'
count = 0
for char in char_tuple:
    if char in vowels:
        count += 1
print(f"Number of vowels: {count}")
