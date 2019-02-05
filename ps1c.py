"""
Problem Set 1c
Name: Griffin Leonard
Collaborators: n/a
Time Spent: 1:40
"""
initial_deposit = float(input('Enter the initial deposit: '))
total_cost = float(950000)
portion_down_payment = 0.32
low = 0
high = 10000
error = 100
down_payment = total_cost*portion_down_payment
current_savings = initial_deposit
steps = 0

while abs(down_payment-current_savings) >= error:
    r = (high+low)//2
    current_savings = initial_deposit*(1+r/120000)**36
    if current_savings > down_payment + 100:
        high = r
    if current_savings < down_payment - 100:
        low = r
    best_r = r/10000
    steps += 1
    if initial_deposit*(1+high/120000)**36 < down_payment - 100:
        best_r = str('It is not possible to pay the down payment in three years.')
        break
print('Best savings rate:', best_r)
print('Steps in bisection search:', steps)