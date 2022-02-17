import matplotlib.pyplot as plt

with open("data.txt") as file:
    data = [float(line.rstrip()) for line in file]

plt.plot(data)
plt.show()
