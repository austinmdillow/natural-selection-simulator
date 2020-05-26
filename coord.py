class Coord:
  def __init__(self, x, y, direction):
    self.x = x
    self.y = y
    self.dir = direction
  
  def update(self, x, y, direction):
    self.x = x
    self.y = y
    self.dir = direction
  
  def updateXY(self, x, y):
    self.x = x
    self.y = y
  