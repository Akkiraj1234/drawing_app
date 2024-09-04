from tkinter import Canvas
from ttkbootstrap import *

class Params:
    def __init__(self) -> None:
        self.default_data()
    
    def default_data(self) ->None:
        self.minimum_size_width = 700
        self.minimum_size_height = 400
        
        self.TOOLBAR_WIDTH = 50
        self.RIGHT_HAND_WIDth = 200
        self.toolbar_idel_height = 340 #toolbar height will be fixed thats why
        self.PADDINGX = 58 #thease are fixed and calculated dont chnage it until found a method
        self.PADDINGY = 22 #thease are fixed and calculated dont chnage it until found a method
        
        self.new_x = 0
        self.new_y = 0
        
        self.current_color = None
        
        self.text_style1 = {}


params = Params()

        
    