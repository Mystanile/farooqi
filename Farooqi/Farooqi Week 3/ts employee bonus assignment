#employee bonus assignment using dictionaries
employees = {}

# Input employees and their salaries
while True:
    name = input("Enter employee name (or 'done' to finish): ")
    if name.lower() == 'done':
        break
    salary = float(input(f"Enter salary for {name}: "))
    employees[name] = salary
    print(employees)

for name, salary in employees.items():
    if salary > 80000:
        bonus_percentage = 10
    elif 50000 <= salary <= 80000:
        bonus_percentage = 15
    else:
        bonus_percentage = 20
    
    bonus_amount = salary * bonus_percentage / 100
    final_salary = salary + bonus_amount
    
    print(f"Employee: {name}, Salary: ${salary}, Bonus: {bonus_percentage}%, Final Salary: ${final_salary}")