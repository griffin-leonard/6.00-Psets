"""
Problem Set 1a
Name: Griffin Leonard
Collaborators: n/a
Time Spent: 1:00
"""

annual_salary = float(input('Enter your annual salary: '))
portion_saved = float(input('Enter the portion of your salary you save, as a decimal: '))
total_cost = float(input('Enter the cost of your dream home: '))
portion_down_payment = 0.18
current_savings = 0.0
r = 0.03
months = 0

down_payment = total_cost*portion_down_payment
monthly_savings = annual_salary*portion_saved/12

while current_savings < down_payment:
    months += 1
    current_savings += monthly_savings + current_savings*r/12
print('Number of months:', int(months))