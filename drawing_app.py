from tkinter import Canvas,Tk,StringVar,Toplevel
import ttkbootstrap as ttk
from webbrowser import open as open_link
import re
from PIL import Image, ImageTk, ImageDraw

class text_obj:
    def __init__(self, canvas:Canvas) -> None:
        self.canvas = canvas
        self.the_id = None
        self.mark = {'x':0, 'y':0}
        self.__inisialize()

    def __inisialize(self):
        self.frame = ttk.Frame(self.canvas,border=3,cursor='fleur')
        self.button1 = ttk.Button(self.frame,cursor='hand2',text='✘',width=2,command=self.delete)
        self.button2 = ttk.Button(self.frame,cursor='hand2',text='✔',width=2,command=self.get_data)
        self.entry = ttk.Entry(self.frame)
        self.entry.grid(row=0,column=0)
        self.button1.grid(row=0,column=1)
        self.button2.grid(row=0,column=2)
        self.frame.bind("<Button-1>",self.move)
        self.frame.bind("<B1-Motion>", self.motion_move)
    
    def move(self,event):
        self.mark = {"x": event.x, "y": event.y}
    
    def motion_move(self,event):
        x , y = self.mark['x'] - event.x, self.mark['y'] - event.y
        ccoords = self.canvas.coords(self.the_id)
        
        self.canvas.coords(self.the_id,ccoords[0] - x ,ccoords[1]- y)
    
    def create(self, event):
        if self.the_id is not None:
            self.canvas.bell
            return 
         
        self.entry.delete(0,ttk.END)
        self.the_id = self.canvas.create_window(
            event.x,event.y,anchor='center',
            window = self.frame
        )
        return self.the_id
    
    def delete(self):
        if self.the_id is None:
            return
        
        self.canvas.delete(self.the_id)
        
        self.the_id = None
    
    def get_data(self):
        text = self.entry.get()
        coords=self.canvas.coords(self.the_id)
        width = self.frame.winfo_width() // 2
        height = self.frame.winfo_height() // 2
        
        coords = (coords[0] - width + 10, coords[1] - height + 10)
        color = window.current_color
        self.delete()
        
        self.canvas.image_draw.text(coords, text=text, fill=color)
        self.canvas.update_image()

class shape_obj:
    def __init__(self,canvas:Canvas) -> None:
        self.canvas = canvas
        self.the_id = None
        self.mark = {'x':0, 'y':0}
        self.__add_styling()
        self.__inisialize()
        self.__grid_up()
        self.setup()

        
    def __add_styling(self):
        self.button_style = ttk.Style()
        self.button_style.configure('SmallButton.TButton', padding=[5, 0], relief='flat', height=1)
        
    def __inisialize(self) -> None:
        #creating all the widgetes
        self.mainframe = ttk.Frame(self.canvas, border=3, cursor='fleur', relief='raised')
        self.frame = ttk.Frame(self.mainframe, cursor="arrow", relief="flat")
        
        self.close_button = ttk.Button(self.frame, cursor='hand2', text='✘',width=2,  style="SmallButton.TButton")
        self.save_button  = ttk.Button(self.frame, cursor='hand2', text='✔',width=2,  style="SmallButton.TButton")
        self.remove_shape = ttk.Button(self.frame, cursor='hand2', text='remove shape',style="SmallButton.TButton")
        
        self.canvas_frame = ttk.Frame(self.frame, border=1, relief='raised', cursor = '')
        self.canvas1 = Canvas(self.canvas_frame, width=130, height=40,cursor='hand2')
        self.canvas_scrollbar = ttk.Scrollbar(self.canvas_frame,orient='horizontal')
        
        self.fill_frame = ttk.Frame(self.frame, border=1, cursor = '')
        self.fill_label = ttk.Label(self.fill_frame, text="fill", font=('arial',10))
        self.fill_ceck = ttk.Checkbutton(self.fill_frame, offvalue=False, onvalue=True, cursor='hand2')
        
        self.width_lable = ttk.Label(self.frame, text='width : 00', font=('arial',10))
        self.width_size = ttk.Scale(self.frame, orient='horizontal', cursor='hand2', length=130)
        
        self.color1 = ttk.Label(self.frame, text='border color',font=('arial',10))
        self.color2 = ttk.Label(self.frame, text='fill color', font=('arial',10))
        self.color1_icon = ttk.Label(self.frame, background='white', width=2, cursor='hand2')
        self.color2_icon = ttk.Label(self.frame, background='green', width=2, cursor='hand2',  relief='ridge')
    
    def __grid_up(self) -> None:
        #griding up 
        self.frame.pack()
        self.remove_shape.grid(row=0, column=0)
        self.save_button.grid( row=0, column=1)
        self.close_button.grid(row=0, column=2)
        
        self.canvas_frame.grid(row=1, column=0, columnspan=3)
        self.canvas1.grid(row=0,column=0)
        self.canvas_scrollbar.grid(row=1,column=0, sticky='nwse')
        
        self.width_lable.grid(row=2, column=0, sticky='w', padx=5)
        self.fill_frame.grid(row=2, column=1, columnspan=2)
        self.fill_label.grid(row=0, column=0, padx=3)
        self.fill_ceck.grid(row=0, column=1, padx=3)
        
        self.width_size.grid(row=3, column=0, columnspan=3)
        
        self.color1.grid(row=4, column=0, sticky='w', padx=5)
        self.color1_icon.grid(row=4, column=1, columnspan=2)
        
        self.color2.grid(row=5, column=0, sticky='w', padx=5)
        self.color2_icon.grid(row=5, column=1, columnspan=2)
    
    def setup(self) -> None:
        self.close_button.config(command=None)
        self.save_button.config(command=None)
        self.remove_shape.config(command=None)
        
        self.defult()
        #conecting the canvas to the scrollbar
        self.canvas1.configure(scrollregion=self.canvas1.bbox('all'))
        self.canvas_scrollbar.config(command=self.canvas1.xview)
        self.canvas1.config(xscrollcommand=self.canvas_scrollbar.set)
        
    def defult(self) -> None:
        x1 , y1 = 10, 10
        for _ in range(10):
            self.canvas1.create_rectangle(
                x1 , y1 ,
                x1 + 40,
                y1 + 35,
                outline= 'white'
            )
            x1 += 40 + 10
    
    def create(self, event) -> None:
        self.the_id = self.canvas.create_window(
            event.x , event.y , anchor='center',
            window = self.mainframe, tags='on_top1'
        )
        self.canvas.tag_raise('on_top1 ')
        
    
    def resize(self) -> None:
        pass

    pass


class canvas(Canvas):
    def __init__(self, root: ttk.Window):
        super().__init__(root,cursor='pencil')
        #'circle' for eraaser 
        self.root = root
        self.points = []
        self.image_position = [0, 0]  # Initial image position
        self.drag_data = {"x": 0, "y": 0}  # To store dragging position
        self.text = text_obj(self)
        self.shape_obj = shape_obj(self)
        
        self.create_image_obj()
        
    def creting_a_text_window(self,event) -> tuple:
        self.text.create(event)
    
    def __fix_coords(self,coords) -> tuple[int]:
        x = coords[0] - self.image_position[0]
        y = coords[1] - self.image_position[1]
        return x,y

    def create_image_obj(self):
        self.width_img, self.height_img = 2000, 1500
        bg_color = ttk.Style().lookup(self.root.winfo_class(), 'background')
        
        self.image = Image.new("RGBA", (self.width_img, self.height_img), bg_color)
        self.image_draw = ImageDraw.Draw(self.image)
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.image_id = self.create_image(self.image_position[0], self.image_position[1], anchor="nw", image=self.photo_image)
        
    def start_paint(self, event, fill = (0,0,0,0)):
        # Initialize point list when mouse button is pressed
        x , y =self.__fix_coords((event.x,event.y))
        
        self.image_draw.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=fill)
        self.update_image()
        self.points = [(x, y)]

    def paint(self, event, fill = (0,0,0,0)):
        x , y =self.__fix_coords((event.x,event.y))
        # Add the current position to the list
        self.points.append((x, y))

        if len(self.points) < 2:
            return

        # Draw a line from the last point to the current point
        self.draw_interpolated_line(self.points[-2], self.points[-1], fill= fill)

        # Update the displayed portion of the image
        self.points.pop(0)
        self.update_image()
    
    def draw_interpolated_line(self, p1, p2, fill = None):
        if fill == None:
            fill=window.current_color
        # Simple linear interpolation to draw a line between two points
        self.image_draw.line([p1, p2], fill = fill, width=3, joint="curve")

    def draw_catmull_rom_spline(self, p0, p1, p2, p3, fill = None):
        if fill is None:
            fill=window.current_color
        # Draw a Catmull-Rom spline from p1 to p2 using p0 and p3 as control points
        old = None
        for t in range(0, 101):  # Adjust granularity by changing range or step
            t = t / 100.0
            # Catmull-Rom formula
            x = 0.5 * ((-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t**3 +
                       (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t**2 +
                       (-p0[0] + p2[0]) * t +
                       2 * p1[0])
            y = 0.5 * ((-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t**3 +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t**2 +
                       (-p0[1] + p2[1]) * t +
                       2 * p1[1])
            if old:
                self.image_draw.line([old, (x, y)], fill=fill, width=3)
            old = (x, y)
    
    def start_move(self, event) -> None:
        # Record the starting position of the drag
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def move(self, event) -> None:
        # Compute the difference in movement
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]

        # Update the position of the image
        self.image_position[0] += delta_x
        self.image_position[1] += delta_y

        # Update the dragging data for the next motion event
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

        # Move the image on the canvas
        self.update_image()
        self.coords(self.image_id, self.image_position[0], self.image_position[1])

    def update_image(self):
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        # Crop the large image to fit the current canvas size
        x = self.image_position[0]
        y = self.image_position[1]
        self.photo_image = ImageTk.PhotoImage(self.image.crop((0, 0, self.width - x, self.height - y)))
        self.itemconfig(self.image_id, image=self.photo_image)


class toolbar(Canvas):
    def __init__(self,root:Tk):
        super().__init__(
            master = root,
        )
        self.values = [
            'pen','move','eraser','text','shape','droper','eye_droper'
        ]
        self.current_coords = []
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
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        devide = self.width // 5
        self.__padx = devide // 2
        self.__xbox_size = devide * 4
        self.__ybox_size = self.height // 8
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
    
    def _inside(self, coords, x,y):
        return coords[0] < x < coords[2] and coords[1] < y < coords[3] 
    
    def current_tool(self, event) -> str:
        if not self.current_coords:
            return None
        
        x = event.x
        y = event.y
        
        for n, coords in enumerate(self.current_coords):
            if self._inside(coords, x,y):
                return self.values[n]
            
    def resize(self) -> None:
        self.__calculation()
        startx = self.__padx
        starty = self.__pady
        
        #creating first tool (pen tool)
        coords = (startx, starty, startx+self.__xbox_size, starty+self.__ybox_size)
        self.coords(self.rectangle_shapes[0], coords)
        self.__create_pen(self.rectangle_shapes[7],self.polygon_shapes[0],startx,starty)
        self.current_coords.append(coords)
        
        # creating secoend tool (move tool)
        starty += self.__pady + self.__ybox_size
        coords = (startx, starty, startx+self.__xbox_size, starty+self.__ybox_size)
        self.coords(self.rectangle_shapes[1], coords)
        self.__create_plus(self.line_shapes[0],self.line_shapes[1],startx,starty)
        self.current_coords.append(coords)
        
        #creating third tool (erase tool)
        starty += self.__pady + self.__ybox_size
        coords = (startx, starty, startx+self.__xbox_size, starty+self.__ybox_size)
        self.coords(self.rectangle_shapes[2], coords)
        self.__create_eraser(self.rectangle_shapes[8],self.rectangle_shapes[9],startx,starty)
        self.current_coords.append(coords)
        
        #creating forth tool (text tool)
        starty += self.__pady + self.__ybox_size
        coords = (startx, starty, startx+self.__xbox_size, starty+self.__ybox_size)
        self.coords(self.rectangle_shapes[3], coords)
        self.__create_text(self.line_shapes[2],self.line_shapes[3],startx,starty)
        self.current_coords.append(coords)
        
        #creating fifth tool (shape tool)
        starty += self.__pady + self.__ybox_size
        coords = (startx, starty, startx+self.__xbox_size, starty+self.__ybox_size)
        self.coords(self.rectangle_shapes[4], coords)
        self.__create_shape(self.rectangle_shapes[10],self.polygon_shapes[1],startx,starty)
        self.current_coords.append(coords)
        
        #creating sixth tool (droper tool)
        starty += self.__pady + self.__ybox_size
        coords = (startx, starty, startx+self.__xbox_size, starty+self.__ybox_size)
        self.coords(self.rectangle_shapes[5], coords)
        self.__create_droper(self.rectangle_shapes[11],self.polygon_shapes[1],startx,starty)
        self.current_coords.append(coords)
        
        #creating seventh tool (eye droper tool)
        starty += self.__pady + self.__ybox_size
        coords = (startx, starty, startx+self.__xbox_size, starty+self.__ybox_size)
        self.coords(self.rectangle_shapes[6], coords)
        self.__create_eyes_droper(self.rectangle_shapes[12],self.polygon_shapes[1],startx,starty)
        self.current_coords.append(coords)


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


class pencils(Canvas):
    def __init__(self, root:Tk):
        super().__init__(
            master = root,
            background = '#000000',
        )


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
        # self.canvas_widget.inisial()
        
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
        
        self.current_brush = None
        
        self.perfect_line = None
        
        self.brush_size = None
        
        self.current_tool = None
        
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
        self.current_tool = 'pen'#add lighting from here
    
    def canvas_binding_method_on_motion(self,event):
        tool_selcted = self.current_tool
        color = self.current_color
        
        if tool_selcted == 'pen':
            self.canvas_widget.paint(event, self.current_color)
        elif tool_selcted == 'move':
            self.canvas_widget.move(event)
        elif tool_selcted == 'eraser':
            self.canvas_widget.paint(event)#eraseer
    
    def canvas_binding_method_on_click(self, event):
        tool_selcted = self.current_tool
        if tool_selcted == 'pen':
            self.canvas_widget.start_paint(event,self.current_color)
        elif tool_selcted == 'move':
            self.canvas_widget.start_move(event)
        elif tool_selcted == 'eraser':
            self.canvas_widget.start_paint(event)#eraser
        elif tool_selcted == 'text':
            self.canvas_widget.creting_a_text_window(event)
        elif tool_selcted == 'shape':
            self.canvas_widget.shape_obj.create(event)
            
    
    def connecting_tools(self):
        def set_current_color(event):
            self.current_color = self.color_plate_widget.get_color(event)
            print(self.current_color,event.x)
        
        def set_current_tool(event):
            self.current_tool = self.toolbar_widget.current_tool(event)
            print('u not hidden', self.current_tool)
        
        #adding color to the color plate
        self.get_hascolro.button.bind('<Button-1>',lambda event: self.after_idle(
            self.color_plate_widget.add_color,self.get_hascolro.get)
        )
        #getting current color
        self.color_plate_widget.bind('<Button-1>',lambda event: self.after_idle(
            set_current_color, event)
        )
        #getting current tool
        self.toolbar_widget.bind("<Button-1>",lambda event: self.after_idle(
            set_current_tool, event)
        )
        
        #canvas binding
        self.canvas_widget.bind("<Button-1>",self.canvas_binding_method_on_click)
        self.canvas_widget.bind("<B1-Motion>", self.canvas_binding_method_on_motion)
        
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
        self.after_idle(self.canvas_widget.update_image)

if __name__ == '__main__':
    window = root(700,400)
    window.mainloop()