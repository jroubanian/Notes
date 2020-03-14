# tuples are lists that cannot be changed
weekend = ('Saturday', 'Sunday')
workweek = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')

humpday = workweek[2]

daysoftheweek = workweek + weekend

print(daysoftheweek)

type(daysoftheweek)
type(humpday)

# a tuple with one item must have a comma following the value
day1 = (1,)

# converts the tuple to a list
list(weekend)

# converts the list to a tuple
tuple(weekend)

# a for loop using tuples
for day in daysoftheweek:
    print(day)

    
(sat,sun) = weekend
print(sat)
print(sun)

# deleting a tuple
test = (1,2,3)
type(test)
del test
test

max(weekend)
max(workweek)

# max/min functions with tuples
test2 = (1,2,3,4)
max(test2)
min(test2)

# max/min functions with a list
test3 = [1,2,3,4]
max(test3)
min(test3)
