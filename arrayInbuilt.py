# array is an inbuilt function in python
import array

# create an array of integers with intial values
a = array.array('i', [1, 2, 3, 4, 5])
print(a) 

# add a new element at end of array
a.append(10)
print(a)

# add another set of elements to array
a.extend([11,12,14])
print(a)

# add a new element in at positon 
a.insert(0,4)  #  Position first and the number to be inserted
print(a)

# remove an element from the array  using the value, here 2 the element itself
a.remove(2)
print(a)

# remove an element from the  array using its position, here 2 is the position 
a.pop(2)
print(a)

# Happy Learning