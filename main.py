import ttkbootstrap as ttk
from drawing_app import (
    canvas,
    toolbar,
    color_plate,
    pencils,
    nevigation,
    get_hascolro,
    pen_size
)



class root(ttk.Window):
    """
    the root window for the method 
    its a ttk.window class that is modified with new method
    for handeling things and root windows
    """
    def __init__(self, width:int, height:int) -> None:
        """_summary_

        Args:
            width (int): _description_
            height (int): _description_
        """
        super().__init__(themename = 'cyborg')
        self.__styles_and_constant()
        
        self.geometry(f'{width}x{height}')
        self.minsize(self.minimum_size_width, self.minimum_size_height)
        
        self.__inisialsetup()
        self.gridup()
        
        #resize the wndows once its vissible :0
        self.update_idletasks()  # Process all pending tasks to render the window
        self.wait_visibility(self)  # Wait until the window is fully visible
        self.resize_method() #then call the resize method.
        #then bind the #configure with resize method binding before window appear lead
        #to unexpected behavior like continnure resizing...
        self.bind('<Configure>',self.resize_method)
        
        self.__inisial_var_setup()
        self.canvas_widget.inisial()
        
    def __styles_and_constant(self):
        '''
        this will conatin elemnts for styling thats it buddy
        '''
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

    def __inisialsetup(self):
        '''
        adding the frame layout for everything. do u understand man
        '''
        #adding canvas widget in a frame and packing it so it can be seen the border
        #changing padding may effect appearance so dont remove padding..
        self.toolbar_frame       = ttk.Frame(self, border = 2, padding = 2, relief = "solid")
        self.canvas_frame        = ttk.Frame(self, border = 2, padding = 2, relief = "solid")
        self.righthand_frame     = ttk.Frame(self, border = 2, padding = 2, relief = "solid")
        self.righthand_frame1    = ttk.LabelFrame(self.righthand_frame, border = 1, relief = "sunken", text = 'color plate')
        self.righthand_frame2    = ttk.LabelFrame(self.righthand_frame, border = 1, relief = "sunken", text = 'select pens')
        
        self.nevigation          = nevigation(self)
        self.toolbar_widget      = toolbar(self.toolbar_frame)
        self.canvas_widget       = canvas(self.canvas_frame)
        
        self.color_plate_widget  = color_plate(self.righthand_frame1)
        self.get_hascolro        = get_hascolro(self.righthand_frame1)
        
        self.pencil_widget       = pencils(self.righthand_frame2)
        self.pen_size            = pen_size(self.righthand_frame2)

        self.connecting_tools()
    
    def __inisial_var_setup(self):
        self.current_color = self.color_plate_widget.color_hex_values[0]
    
    def connecting_tools(self):
        def set_current_color(event):
            self.current_color = self.color_plate_widget.get_color(event)
            print(self.current_color,event.x)
        
        self.get_hascolro.button.bind('<Button-1>',lambda event: self.after_idle(
            self.color_plate_widget.add_color,self.get_hascolro.get)
        )
        self.color_plate_widget.bind('<Button-1>',lambda event: self.after_idle(
            set_current_color, event)
        )
        
    def gridup(self):
        #griding the main windows
        self.nevigation.grid(row=0, column=0, columnspan = 3, pady=5)
        self.toolbar_frame.grid(row=1,column=0,padx=5,pady=2,sticky='news')
        self.canvas_frame.grid(row=1,column=1,padx=5,pady=2)
        self.righthand_frame.grid(row=1,column=2,padx=5,pady=2,sticky='news')
        
        #griding the child windows
        self.toolbar_widget.pack(expand=True) #making it expend to move down and up
        self.canvas_widget.pack()
        
        self.righthand_frame1.grid(row=0,column=0)
        self.righthand_frame2.grid(row=1,column=0)
        
        self.color_plate_widget.grid(row=0,column=0)
        self.get_hascolro.grid(row=1,column=0)
        
        self.pencil_widget.grid(row=0,column=0)
        self.pen_size.grid(row=1,column=0)
    
    def resize_method(self,event = None) -> None:
        """
        resize window according to the current root size
        """ 
        cxsize = self.winfo_width()
        cysize = self.winfo_height()
        button_height = self.nevigation.winfo_height()
        
        if self.new_x == cxsize and self.new_y == cysize:
            return None
        
        self.new_x = cxsize
        self.new_y = cysize
        
        #calculating things for resizing in size - 18 becouse of padding took in tottal
        idel_height  = cysize - button_height - self.PADDINGY
        canvas_width = cxsize - self.TOOLBAR_WIDTH - self.RIGHT_HAND_WIDth - self.PADDINGX
        size = (idel_height - (self.PADDINGX - 18) - self.get_hascolro.winfo_height() - self.pen_size.winfo_height())//3
        
        #updation
        self.toolbar_widget.config(width = self.TOOLBAR_WIDTH, height = self.toolbar_idel_height)
        self.canvas_widget.config(width = canvas_width, height = idel_height)
        
        #the right hand widgets updation(color plater, brush plater)
        self.color_plate_widget.config(width = self.RIGHT_HAND_WIDth, height = size*2)
        self.pencil_widget.config(width = self.RIGHT_HAND_WIDth, height = size)
        
        #calling importand methods 
        self.after(200,lambda: self.after_idle(self.toolbar_widget.resize))
        self.after(200,lambda: self.after_idle(self.color_plate_widget.resize))

if __name__ == '__main__':
    win = root(200,200)
    win.mainloop()