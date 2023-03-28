import sys
import random
import matplotlib

matplotlib.use('Qt5Agg')


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# ---------------------------------
#for history team
#import matplotlib.pyplot as plt
#
#fig, ax = plt.subplots()
#
#fruits = ['apple', 'blueberry']
#counts = [40, 100]
#bar_labels = ['red', 'blue', ]
#bar_colors = ['tab:red', 'tab:blue']
#
#ax.bar(fruits, counts, label=bar_labels, color=bar_colors)
#
#ax.set_ylabel('fruit supply')
#ax.set_title('Fruit supply by kind and color')
#ax.legend(title='Fruit color')
#
#plt.show()
#----------------------------------
# for form team
#import matplotlib.pyplot as plt
#import numpy as np
#
#
## Fixing random state for reproducibility
#np.random.seed(19680801)
#
#
#x, y = np.random.randn(2, 100)
#fig, [ax1, ax2] = plt.subplots(2, 1, sharex=True)
#ax1.xcorr(x, y, usevlines=True, maxlags=50, normed=True, lw=2)
#ax1.grid(True)
#
#ax2.acorr(x, usevlines=True, normed=True, maxlags=50, lw=2)
#ax2.grid(True)
#
#plt.show()
# ------------------------------------
#for history match
#import matplotlib.pyplot as plt
#from matplotlib.collections import EventCollection
#
#
## split the data into two parts
#xdata1 = [1, 5, 7, 8, 9, 14, 15, 17, 17, 19]
#xdata2 = [1, 6, 7, 8, 11, 14, 15, 17, 17, 21]
#
#
## plot the data
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)
#ax.plot(xdata1, color='tab:blue')
#ax.plot(xdata2, color='tab:orange')
#ax.set_facecolor('xkcd:salmon')
#ax.set_facecolor(('#5F5F5F'))
#
#ax.set_title('line plot with data points')
#
## display the plot
#plt.show()
# ------------------------------------------
