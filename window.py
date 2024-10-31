import numpy as np
import cv2
from observer import Observer

class Window(Observer):
        
    def __init__(self):
        self.__displayable_object = None
        self.__window = cv2
        self.__keep_displaying = True
            
    def dispose(self):
        self.__window.destroyAllWindows()
        
    def update(self, displayable_force=None):
        self.__displayable_object = displayable_force
        self.__display(self.__displayable_object)
        
    def displayable(self):
        return self.__keep_displaying
    
    def __display(self, frame):   
        if self.__displayable_object is not None:
            self.__window.imshow('Labo 6', self.__displayable_object)
            key = cv2.waitKey(1)
            if key == ord('x'):
                self.__keep_displaying = False