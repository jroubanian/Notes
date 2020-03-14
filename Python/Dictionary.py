# Create a dictionary
contacts = {'John': '646-628-6184', 'Linda': '917-806-7293'}

# creates a variable using the contacts dictionary and the keys
johns_number = contacts['John']
lindas_number = contacts['Linda']

print('Dial {} to call John.'.format (johns_number))
print('Dial {} to call Linda.'.format (lindas_number))

# adds a key:value pair to the contacts dictionary
contacts['Gabrielle'] = '647-282-8159'

# prints contacts
print(contacts)

# prints the length of the contacts dictionary (each key/pair is 1)
print(len(contacts))

# deletes an item from the dictionary
del contacts['John']

print(contacts)

contacts['John'] = '646-628-6184'

print(contacts)


print(contacts.keys())
print(contacts.values())

print('646-628-6184' in contacts.values())

print('Linda' in contacts.keys())
print('Larry' in contacts.keys())

for numbers in contacts:
    print(contacts.values())
    
for contact in contacts:
    print(contacts.keys())    

    
contacts['John'] = 'email' : 'jroubanian@gmail.com' , 'phone' : '646-628-6184'
