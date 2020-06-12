import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/austin/Github/natural-selection-simulator/lib/')
from pylive.pylive import live_plotter
import numpy as np

size = 100
x_vec = np.linspace(0,1,size+1)[0:-1]
y_vec = np.random.randn(len(x_vec))
line1 = []
while True:
    rand_val = np.random.randn(1)
    y_vec[-1] = rand_val
    line1 = live_plotter(x_vec,y_vec,line1)
    y_vec = np.append(y_vec[1:],0.0)