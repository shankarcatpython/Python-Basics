# List the folders in which the python interpreter will search for modules ( *import )

import sys

# print all the path

for value in sys.path:
    print(value)

# print(dir(sys))