from utils import Window, Frame, params

from nevigation import Nevigation_Frame
from toolbar import ToolBar
from canvas import Main_Canvas
from color_plate import Color_Plate
from pencil_plate import Pencil_Plate

class root(Window):
    """
    the root window for the method 
    its a ttk.window class that is modified with new method
    for handeling things and root windows
    """
    def __init__(self, width:int, height:int) -> None:
        """
        set up the root window for the application

        Args:
            width (int): the width of the main root
            height (int): the height of the main root
        """
        super().__init__(
            title = "drawing app",
            themename = 'cyborg'
        )
        
        self.geometry(f'{width}x{height}')
        self.minsize(params.minimum_size_width, params.minimum_size_height)
        self.__initialize_setup()
        self.__seting_up_widegt()

    def __initialize_setup(self):
        self.toolbar_frame       = Frame(self, border = 2, padding = 2, relief = "solid")
        self.canvas_frame        = Frame(self, border = 2, padding = 2, relief = "solid")
        self.righthand_frame     = Frame(self, border = 2, padding = 2, relief = "solid")
    
    def __seting_up_widegt(self):
        self.nevigation          = Nevigation_Frame(self)
        self.toolbar_widget      = ToolBar(self.toolbar_frame)
        self.canvas_widget       = Main_Canvas(self.canvas_frame)
        self.color_plate_frame   = Color_Plate(self.righthand_frame)
        self.pencil_plate_frame  = Pencil_Plate(self.righthand_frame)
    
    def gridup(self):
        #griding the main windows
        self.nevigation.grid(row=0, column=0, columnspan = 3, pady=5)
        self.toolbar_frame.grid(row=1,column=0,padx=5,pady=2,sticky='news')
        self.canvas_frame.grid(row=1,column=1,padx=5,pady=2)
        self.righthand_frame.grid(row=1,column=2,padx=5,pady=2,sticky='news')
        
        #griding the child windows
        self.toolbar_widget.pack(expand=True)
        self.canvas_widget.pack()
        
        self.color_plate_frame.grid(row=0,column=0)
        self.pencil_plate_frame.grid(row=1,column=0)
    


if __name__ == '__main__':
    main = root(700,400)
    main.gridup()
    
    main.mainloop()
    
    