import numpy as np
import matplotlib.pyplot as pl


x = np.linspace(0,10,50)
y = 2.5 * x + 1.2
pl.clf()
pl.plot(x,y,'s')
pl.show()

