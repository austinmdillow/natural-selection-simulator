from enum import Enum
class Species(Enum):
  Rabbit = 1
  Fox = 2
  Carrot = 3
  
  @staticmethod
  def predator(spec):
    if (spec == Species.Rabbit):
      return Species.Fox
    else:
      return None
  
  @staticmethod
  def prey(spec):
    if (spec == Species.Rabbit):
      return Species.Carrot
    elif (spec == Species.Fox):
      return Species.Rabbit
    else:
      return None

  @staticmethod
  def food(spec):
    if (spec == Species.Rabbit):
      return Species.Carrot
    elif (spec == Species.Fox):
      return Species.Rabbit
    else:
      return None