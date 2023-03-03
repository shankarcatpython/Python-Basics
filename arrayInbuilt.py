import array

a = array.array('i', [1, 2, 3, 4, 5])
print(a) 

a.append(10)
print(a)

a.extend([11,12,14])
print(a)

a.insert(0,4)  #  Position first and the number to be inserted
print(a)

a.remove(2)
print(a)