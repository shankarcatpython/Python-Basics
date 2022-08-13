'''
Simple program to display start and end time also a for loop
'''
import time

print('Hello')

print( "Start Time {}".format(time.ctime()))

for i in range(1,5):
    print("Hello with in the for loop")
    time.sleep(3)

print( "Endtime Time {}".format(time.ctime()))