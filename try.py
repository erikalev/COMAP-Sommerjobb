import matplotlib.pyplot as plt

fig, ((ax1, ax2), (ax3, ax4))= plt.subplots(2, 2, subplot_kw=dict(projection='aitoff'))
ax1.plot(range(12))
ax2.plot(range(10))
ax3.plot(range(8))
ax4.plot(range(6))
plt.show()
