import logging

from PCA9685 import PCA9685

class Servo():
    def __init__(self, name, pca:PCA9685, frequency, channel, min, max, center):
        self.logger = logging.getLogger('MarsRover.Servo')
        self.name = name
        self.frequency = frequency
        self.pca = pca

    def setPWM(self, on, off):{
        
    }

    def toMin():{

    }

    def toMax():{

    }

    def toCenter():{
        
    }
    
    def dispatch():{

    }
    
    def setFrequency(self, newFrequency):{
        self.frequency == newFrequency
    }
