from tkinter import Canvas,Tk,StringVar,Toplevel
import ttkbootstrap as ttk
from webbrowser import open as open_link
import re


class canvas(Canvas):
    def __init__(self,root):
        super().__init__(root)
        
    def inisial(self):
        box_size = 5
        self.create_oval(100,100,100 + box_size,100 + box_size,fill='white')
        
        print((self.winfo_height() // box_size) * (self.winfo_width() // box_size))
    
    def inisial_advance(self):
        height = self.winfo_height()
        width  = self.winfo_width()
        
        x = y = 0
        box_size = 5
        
        num = 1
        while y <= height:
            while x <= width:
                self.create_oval(x,y,x+box_size,y+box_size,fill='white')
                x += box_size
                if num >= 200:
                    return
                num += 1
            y+=box_size
            x = 0
            


class toolbar(Canvas):
    def __init__(self,root:Tk):
        super().__init__(
            master = root,
        )
        self.__add_elements()
    
    def __add_elements(self) -> None:
        self.rectangle_shapes = [
            self.create_rectangle(0,0,0,0,outline='blue',width=3)
            for _ in range(13)
        ]
        
        self.line_shapes = [
            self.create_line(0,0,0,0,joinstyle='round',capstyle='round',width=3) 
            for _ in range(4)
        ]
        
        self.polygon_shapes = [
            self.create_polygon(0,0,0,0,0,0,outline='blue',joinstyle='round')
            for _ in range(2)
        ]
    
    def __calculation(self) -> None:
        width = self.winfo_width()
        height = self.winfo_height()
        devide = width // 5
        self.__padx = devide // 2
        self.__xbox_size = devide * 4
        self.__ybox_size = height // 8
        self.__pady = self.__ybox_size // 8
        
    def __create_pen(self, id1, id2, x1, y1) -> None:
        # Calculate center position of the region
        center_x = x1 + self.__xbox_size // 2
        center_y = y1 + self.__ybox_size // 2

        # Dimensions for the pen body (rectangle)
        pen_body_width = self.__xbox_size // 6  # Narrow rectangle
        pen_body_height = self.__ybox_size // 2

        # Set coordinates for the rectangle (pen body)
        self.coords(id1,
            center_x - pen_body_width // 2, center_y - pen_body_height // 2,
            center_x + pen_body_width // 2, center_y + pen_body_height // 2
        )

        # Position the pyramid (pen nib) below the pen body
        pyramid_height = self.__ybox_size // 6
        pyramid_base = pen_body_width

        # Calculate points for the pyramid (pen nib)
        pyramid_points = [
            center_x - pyramid_base // 2, center_y + pen_body_height // 2,  # Bottom left
            center_x + pyramid_base // 2, center_y + pen_body_height // 2,  # Bottom right
            center_x, center_y + pen_body_height // 2 + pyramid_height  # Top point
        ]

        # Set coordinates for the pyramid
        self.coords(id2, *pyramid_points)

        # Adjust styling for the pen
        self.itemconfig(id1, outline='white',width = 2)  # Pen body
        self.itemconfig(id2, fill='white', outline='white')  # Pen nib
    
    def __create_plus(self, id1, id2, x1, y1) -> None:
        # Calculate center position of the region
        center_x = x1 + self.__xbox_size // 2
        center_y = y1 + self.__ybox_size // 2
        
        # Calculate line lengths to stay within the box size
        line_length_x = self.__xbox_size // 1.5  
        line_length_y = self.__ybox_size // 1.5
        
        self.coords(id1,
            center_x - line_length_x // 2, center_y, 
            center_x + line_length_x // 2, center_y 
        )
        
        self.coords(id2, 
            center_x, center_y - line_length_y // 2,
            center_x, center_y + line_length_y // 2   
        )
        #adujting styling
        for id in (id2,id1):
            self.itemconfig(id,
            arrow='both',
            arrowshape=(6, 5, 4),
            fill='white'
        )

    def __create_eraser(self, id1, id2, x1, y1) -> None:
        # Calculate center position of the region
        center_x = x1 + self.__xbox_size // 2
        center_y = y1 + self.__ybox_size // 2

        # Dimensions for the main eraser body
        eraser_width = self.__xbox_size // 4
        eraser_height = self.__ybox_size // 2

        # Set coordinates for the main eraser body (id1)
        self.coords(id1,
            center_x - eraser_width // 2, center_y - eraser_height // 2,
            center_x + eraser_width // 2, center_y + eraser_height // 2
        )

        # Dimensions for the eraser's band (id2)
        band_width = eraser_width
        band_height = eraser_height // 2

        # Set coordinates for the band (id2), positioned at one end of the main body
        self.coords(id2,
            center_x - band_width // 2, center_y - eraser_height // 2,
            center_x + band_width // 2, center_y - eraser_height // 2 + band_height
        )

        # Adjust styling for the eraser and its band
        self.itemconfig(id1, fill='black', outline='white')  # Main eraser body
        self.itemconfig(id2,fill='white', outline='white',width = 2)   # Band
    
    def __create_text(self,id1,id2,x1,y1) -> None:
        # Calculate center position of the region
        center_x = x1 + self.__xbox_size // 2
        center_y = y1 + self.__ybox_size // 2

        # Dimensions for the vertical and horizontal parts of the "T"
        t_width = self.__xbox_size // 4
        t_height = self.__ybox_size // 2

        # Coordinates for the horizontal part of the "T"
        horizontal_start_x = center_x - t_width // 2
        horizontal_end_x = center_x + t_width // 2
        horizontal_y = center_y - t_height // 4

        # Coordinates for the vertical part of the "T" (id1)
        vertical_start_x = center_x
        vertical_start_y = center_y - t_height // 2
        vertical_end_y = center_y + t_height // 2

        # Set coordinates for the horizontal part (line)
        self.coords(id1, horizontal_start_x, horizontal_y, horizontal_end_x, horizontal_y)

        # Set coordinates for the vertical part (line)
        self.coords(id2, vertical_start_x, vertical_start_y, vertical_start_x, vertical_end_y)

        # Adjust styling for the "T" lines
        self.itemconfig(id1, fill='white', width=2)  # Horizontal line
        self.itemconfig(id2, fill='white', width=2)  # Vertical line
    
    def __create_shape(self,id1, id2, x1, y1) -> None:
        # Calculate center position of the region
        center_x = x1 + self.__xbox_size // 2
        center_y = y1 + self.__ybox_size // 2

        # Dimensions for the square
        square_size = self.__xbox_size // 3

        # Set coordinates for the square (id2)
        self.coords(id1,
            center_x - square_size // 2, center_y - square_size // 2,
            center_x + square_size // 2, center_y + square_size // 2
        )

        # Dimensions and coordinates for the triangle (id1)
        triangle_size = self.__xbox_size // 2
        triangle_points = [
            center_x, center_y - triangle_size // 2,          # Top point
            center_x - triangle_size // 2, center_y + triangle_size // 2,  # Bottom left
            center_x + triangle_size // 2, center_y + triangle_size // 2   # Bottom right
        ]

        # Set coordinates for the triangle (id1)
        self.coords(id2, *triangle_points)

        # Adjust styling for the shapes
        self.itemconfig(id1, fill='blue', outline='black')  # Triangle
        self.itemconfig(id2, fill='red', outline='black')   # Square
    
    def __create_droper(self,id1,id2,x1, x2) -> None:
        pass
    
    def __create_eyes_droper(self,id1,id2,x1,x2) -> None:
        pass
    
    def resize(self) -> None:
        self.__calculation()
        startx = self.__padx
        starty = self.__pady
        
        #creating first tool (pen tool)
        self.coords(self.rectangle_shapes[0],
            startx, starty, startx+self.__xbox_size, starty+self.__ybox_size
        )
        self.__create_pen(self.rectangle_shapes[7],self.polygon_shapes[0],startx,starty)
        
        # creating secoend tool (move tool)
        starty += self.__pady + self.__ybox_size
        self.coords(self.rectangle_shapes[1],
            startx, starty, startx+self.__xbox_size, starty+self.__ybox_size
        )
        self.__create_plus(self.line_shapes[0],self.line_shapes[1],startx,starty)
        
        #creating third tool (erase tool)
        starty += self.__pady + self.__ybox_size
        self.coords(self.rectangle_shapes[2],
            startx, starty, startx+self.__xbox_size, starty+self.__ybox_size
        )
        self.__create_eraser(self.rectangle_shapes[8],self.rectangle_shapes[9],startx,starty)
        
        #creating forth tool (text tool)
        starty += self.__pady + self.__ybox_size
        self.coords(self.rectangle_shapes[3],
            startx, starty, startx+self.__xbox_size, starty+self.__ybox_size
        )
        self.__create_text(self.line_shapes[2],self.line_shapes[3],startx,starty)
        
        #creating fifth tool (shape tool)
        starty += self.__pady + self.__ybox_size
        self.coords(self.rectangle_shapes[4],
            startx, starty, startx+self.__xbox_size, starty+self.__ybox_size
        )
        self.__create_shape(self.rectangle_shapes[10],self.polygon_shapes[1],startx,starty)
        
        #creating sixth tool (droper tool)
        starty += self.__pady + self.__ybox_size
        self.coords(self.rectangle_shapes[5],
            startx, starty, startx+self.__xbox_size, starty+self.__ybox_size
        )
        self.__create_droper(self.rectangle_shapes[11],self.polygon_shapes[1],startx,starty)
        
        #creating seventh tool (eye droper tool)
        starty += self.__pady + self.__ybox_size
        self.coords(self.rectangle_shapes[6],
            startx, starty, startx+self.__xbox_size, starty+self.__ybox_size
        )
        self.__create_eyes_droper(self.rectangle_shapes[12],self.polygon_shapes[1],startx,starty)


class color_plate(Canvas):
    def __init__(self,root:Tk):
        super().__init__(
            master = root,
        )
        self.root = root
        self.currenx = 0
        self.curreny = 0
        self.box_size = 25
        
        self.color_hex_values = []
        self.color_id = []
        
        self.scroll_bar = ttk.Scrollbar(
            master = root,
            orient = 'vertical'
        )
        self.__inisalize()
        
    def __inisalize(self) -> None:
        inisial_color = [
            "#FFFFFF", "#FF0000", "#0000FF", "#00FF00", "#FFFF00",
            "#00FFFF", "#FFB6C1", "#FFA500", "#E6E6FA", "#FFFACD",
            "#87CEEB", "#98FB98", "#D3D3D3", "#C0C0C0", "#F5F5DC",
            "#FFD700", "#C0C0C0", "#39FF14"
        ]
        for color in inisial_color:
            self.add_color(color,False)
        self.resize()

    def add_color(self, color:str,update:bool = True) -> None:
        if callable(color):
            color = color()
            
        #check if the hax color is color or not
        if not bool(re.match(r"#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", color)):
            return
        
        if len(self.color_id) > 400:
            return
        
        #creating shape and color
        self.color_hex_values.append(color)
        self.color_id.append(
            self.create_rectangle(
                -1, -1, -1, -1, fill=color
            )
        )
        if update:
            self.resize(update_last=True)
    
    def get_color(self, event) -> str|None:
        x, y = event.x, event.y
        # width , height = self.winfo_width(), self.winfo_height()
        width = self.winfo_width()
        
        x //= (self.box_size + 2) + 1#pading
        y //= (self.box_size + 2) + 1#pading
        width //= (self.box_size + 2) + 1
        # height //= (self.box_size + 2) + 1
        
        ans = (y * width ) + x
        return self.color_hex_values[ans] if len(self.color_hex_values) > ans else None
        
    def resize(self, update_last:bool = False):
        #unviversal var
        other = 0
        padding = 2
        limitx = int(self.cget('width'))
        limity = int(self.cget('height'))
        
        x1 = self.canvasx(0)  # Maps the screen's (0,0) to canvas coordinates
        y1 = self.canvasy(0)
        print(x1,y1)
        
        # implemnting scale
        if self.curreny > limity :
            self.configure(scrollregion=self.bbox("all"))
            self.scroll_bar.grid(row=0,column=1,sticky='ns')
            self.scroll_bar.config(command=self.yview)
            self.config(yscrollcommand=self.scroll_bar.set)
            other = self.scroll_bar.winfo_width()
            limitx -= other
            self.config(width=limitx)
        
        else:
            # Hide scrollbar if not needed
            self.scroll_bar.grid_remove()
            other = 0
        
        #reszing elements if update_last no needa start from begining if not start updation from 0,0
        if (not update_last) or bool(other):
            self.currenx = 0
            self.curreny = 0
        
        for id in [self.color_id[-1]] if update_last else self.color_id:
            
            if self.currenx + self.box_size + padding <= limitx:
                self.currenx += padding
                
            else:
                self.currenx = padding
                self.curreny += self.box_size + padding
            
            # if self.curreny + self.box_size + padding > limity:
            #     return None
            
            self.coords(id,
                self.currenx, self.curreny,
                self.currenx + self.box_size,
                self.curreny + self.box_size,
            )
            self.currenx += self.box_size
   

class pencils(Canvas):
    def __init__(self, root:Tk):
        super().__init__(
            master = root,
            background = '#000000',
        )


class nevigation(ttk.Frame):
    def __init__(self,root:Tk) -> None:
        """
        setting up the export options and widgets 
        its a frame inharited class
        """
        super().__init__(root,relief='flat')
        self.__crating_widgets()
        self.setup()
    
    def export_command(self) -> None:
        format_ = self.export_formats.get()
        print(f'anything but not export{format_}')
    
    def __crating_widgets(self) -> None:
        #seting up the drop down for selecting
        values = ['format','.png','.xbm','.jpg','.bitmap']
        self.export_formats = StringVar(self)
        
        self.button1 = ttk.Button(
            master = self,
            text = 'Save',
            cursor = 'hand2',
            command = self.export_command
        )
        
        self.button2 = ttk.Button(
            master = self,
            text = 'Open',
            cursor = 'hand2',
            command = self.export_command
        )
        
        self.drop_down = ttk.OptionMenu(
            self, self.export_formats,
            *values,direction="below"
        )
        
        #setting up the button for export
        self.button3 = ttk.Button(
            master = self,
            text = 'Export',
            cursor = 'hand2',
            command = self.export_command
        )
        
        self.button4 = ttk.Button(
            master = self,
            text = 'Menu',
            cursor = 'hand2',
            command = self.export_command
        )
        
    def setup(self) -> None:
        self.button1.grid(row=0,column=0)
        self.button2.grid(row=0,column=1)
        self.drop_down.grid(row=0,column=2)
        self.button3.grid(row=0,column=3)   
        self.button4.grid(row=0,column=4)     


class get_hascolro(ttk.Frame):
    def __init__(self,root) -> None:
        super().__init__(root,relief='flat')
        self.__crating_widgets()
        self.setup()
    
    def __crating_widgets(self) -> None:
        self.entry = ttk.Entry(
            master = self,
            width = 5
        )
        self.button = ttk.Button(
            master = self,
            text = 'Add',
            width = 5,
        )
    
    def setup(self):
        self.entry.grid(row=0,column=0)
        self.button.grid(row=0,column=1)
    
    def get(self) -> str:
        value = self.entry.get()
        return value


class pen_size(ttk.Frame):
    def __init__(self,root) -> None:
        super().__init__(root,relief='flat')
        self.__crating_widgets()
        self.setup()
      
    def __crating_widgets(self) -> None:
        self.scale = ttk.Scale(
            master = self,
            from_=0, 
            to=100, 
            length=150,
            command=self.update_text
        )
        self.lable = ttk.Label(
            master = self,
            text = '0%'
        )
    
    def update_text(self,value):
        text = "{:^{}}%".format(int(float(value)),5)
        self.lable.config(text=text)
    
    def setup(self):
        self.scale.grid(row=0,column=0)
        self.lable.grid(row=0,column=1)
    
    def get(self) -> None:
        pass


class root(ttk.Window):
    """
    the root window for the method 
    its a ttk.window class that is modified with new method
    for handeling things and root windows
    """
    def __init__(self,width:int, height:int) -> None:
        """
        all window root setup will be done here :)
        """
        super().__init__(themename='cyborg')
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
        self.after(5000,self.canvas_widget.inisial_advance)
        
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
    window = root(700,400)
    window.mainloop()
    
    
    

# class setting(ttk.Button):
#     def __init__(self, root):
#         super().__init__(
#             master = root,
#             command = self.button_comand,
#             text="⚙️",
#             bootstyle="outline",
#             width=6
#         )
#         self.root = root
        
#     def button_comand(self) -> None:
        
#         self.top_level = ttk.Toplevel(
#             title = 'setting option',
#             resizable = (False,False) 
#         )
        
#         #adding widgets and elemnts
#         main_frame = ttk.Frame(self.top_level, padding=10)
#         main_frame.pack(fill="both", expand=True, padx=10, pady=10)
#         self.add_resize_form_window(main_frame)
        
#         social_media_frame = ttk.LabelFrame(self.top_level, text="My Social Media", padding=10)
#         social_media_frame.pack(fill="both", expand=True, padx=10, pady=10)
#         self.add_social_media_window(social_media_frame)
    
#     def add_resize_form_window(self,frame:ttk.Frame):
#         '''
#         something 
#         '''
#         #registering the command
#         command1 = self.top_level.register(self.entry_widget_validation)
        
#         width_label = ttk.Label(frame, text="Width")
#         height_label = ttk.Label(frame, text="Height")
#         width_entry = ttk.Entry(frame,validate='key', validatecommand = (command1,'%P'))
#         height_entry = ttk.Entry(frame,validate="key",validatecommand = (command1,'%P'))
#         change_size_button = ttk.Button(frame, text="Change Size", 
#             command=lambda: self.root.resize(height_entry.get(),width_entry.get(),(height_entry,width_entry))
#         )
        
#         #grid management
#         width_label.grid(row=0, column=0, padx=5, pady=5)
#         height_label.grid(row=0, column=1, padx=5, pady=5)
#         width_entry.grid(row=1, column=0, padx=5, pady=5)
#         height_entry.grid(row=1, column=1, padx=5, pady=5)
#         change_size_button.grid(row=2, column=0, columnspan=2, pady=10)
        
#     def add_social_media_window(self,frame:ttk.Frame):
#         #adding the widgets
#         twitter_button = ttk.Button(
#             frame, text="Twitter(X)",command=lambda:self.open_social_media(1)
#         )
#         github_button = ttk.Button(
#             frame, text="GitHub",command=lambda:self.open_social_media(2)
#         )
#         linkedin_button = ttk.Button(
#             frame, text="Instagram",command=lambda:self.open_social_media(3)
#         )
        
#         #packing the widgets
#         twitter_button.pack(side="left", padx=5, pady=5, expand=True)
#         github_button.pack(side="left", padx=5, pady=5, expand=True)
#         linkedin_button.pack(side="left", padx=5, pady=5, expand=True)
    
#     def entry_widget_validation(self,full:str) -> bool:
#         if full.isdigit() or full == '':
#             return True
#         else: return False

#     def open_social_media(self,social_media:str) -> None:
#         if social_media == 1:
#             open_link("https://x.com/Akhand_raj_")
#         elif social_media == 2:
#             open_link("https://github.com/Akkiraj1234")
#         elif social_media == 3:
#             open_link("https://www.instagram.com/akki_raj_._/")

# def resize(self,height:str|int, width:str|int, window:tuple[ttk.Entry] = None):
#     self.__internl_resize_method()
    
#     height = (0 if height is str and height == '' else int(height) if height.isdigit() else 0
#                 ) if height is not int else height
#     width = (0 if width is str and width == '' else int(width) if width.isdigit() else 0
#                 ) if width is not int else width
    
#     if not height > self.minimum_size_height:
#         height = self.minimum_size_height
#         if window: 
#             window[0].delete(0,ttk.END)
#             window[0].insert(0,height)
            
#     if not width > self.minimum_size_width:
#         width = self.minimum_size_width
#         if window: 
#             window[1].delete(0,ttk.END)
#             window[1].insert(0,width)