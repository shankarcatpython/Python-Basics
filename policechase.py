import numpy as np 
import matplotlib.pyplot as plt

t = np.linspace(0,40,1000)
print(type(t))

# speed of the robber
d_r = 2.5 * t

# speed of the police - we need to plot the police relative to the robber since he started late there by diffrence is 5
d_p = 3 * (t-5)

# Label the plot along with x and y axis
fig , ax = plt.subplots()
plt.title("Police chase")
plt.xlabel("Time in minutes")
plt.ylabel("Distance")

# Set a limit for the plot 
ax.set_xlim([0,40])
ax.set_ylim([0,100])
ax.plot(t,d_p,c='green')
ax.plot(t,d_r,c='red')

#  additional lines to show the meeting point
plt.axvline(x=30,color='purple',linestyle='--')
plt.axhline(y=75,color='orange',linestyle='--')

plt.show()