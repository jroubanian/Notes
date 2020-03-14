#To open a file in Python, we use the open() function. This function accepts two different arguments (inputs) in the parentheses, always in the following order:

# the name of the file (as a string)
# the mode of working with the file (as a string)

#The open() function returns a File object. This object stores the information we passed in, and allows us to call methods specific to the File class. We can assign the File object to a variable so we can refer to it later:


a = open("example.csv", "r")

# Note that the File object, a, won't contain the actual contents of the file. It's instead an object that acts as an interface to the file and contains methods for reading in and modifying the file's contents
###########################################################################################

# 
a = open("testfile.txt", "r")
b = a.read()
print(b)

# import io
c = open("example.csv", "r")
d = c.read()
print(d)