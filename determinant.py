import matplotlib.pyplot as plt


# Determinant helps to validate how much the area changes when a tranformation is made 

x = [0, 2, 6, 4]
y = [0, 4, 6, 2]


plt.plot(x, y)
plt.fill(x, y, alpha=0.2)
plt.grid(True)
plt.show()