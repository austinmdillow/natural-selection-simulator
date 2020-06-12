from environment import Environment
from species import Species
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg') # <-- THIS MAKES IT FAST!
class DataVisualizer():
  def __init__(self, env):
    self.environments = [env]
    plt.ion()
    plt.show()
    print("Init of Data Visualizer complete")

  def plotPopulations(self):
    plt.clf()
    plt.plot(self.environments[0].population_log[Species.Rabbit])
    #plt.draw()
    plt.pause(0.0001)
    