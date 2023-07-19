import numpy as np 
import matplotlib.pyplot as plt

t = np.linspace(0,40,1000)
print(type(t))

# speed of the robber
d_r = 2.5 * t

# speed of the policd

d_p = 3 * (t-5)

fig , ax = plt.subplots()
plt.title("Police chase")
plt.xlabel("Time in minutes")
plt.ylabel("distaince")
ax.set_xlim([0,40])
ax.set_ylim([0,100])
ax.plot(t,d_p,c='green')
ax.plot(t,d_r,c='red')
plt.show()

