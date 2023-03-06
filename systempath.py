# List the folders in which the python interpreter will search for modules ( *import )

import sys

for value in sys.path:
    print(value)