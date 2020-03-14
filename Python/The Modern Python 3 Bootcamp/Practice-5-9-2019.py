#This is a comment


print("How much do you pay in mortgage each month?")
mortgage_input = input()
mortgage = int(mortgage_input)

print("How much do you pay in maintenance each month?")
maintenance_input = input()
maintenance = int(maintenance_input)

print("How much do you pay in car payments each month?")
car_input = input()
car = int(car_input)

print("How much do you pay in insurance each month?")
insurance_input = input()
insurance = int(insurance_input)

month_total = mortgage + car + insurance + maintenance
year_total = month_total * 12
day_total = year_total / 365
day_total_rounded = round(day_total)
print(f"You pay ${month_total} per month, and ${year_total} per year")
print(f"You pay ${day_total_rounded} per day")
