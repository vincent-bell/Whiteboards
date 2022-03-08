from tkinter import Tk, Canvas, Menu


class WhiteboardInstance(Tk):
	def __init__(self, instantiator):
		super().__init__()
		self.instantiator = instantiator
		self.instantiator.destroy()

		self.current_x, self.current_y = (0,0)
		self.drawing_colour = 'black'


	def __call__(self):
		"""
		method calls self.build when a WhiteboardInstance object is called
		:return: None
		"""
		self.build()


	def close_window(self):
		"""
		method to call when window is closed
		:return: None
		"""
		self.instantiator.base_widget.enable()
		self.destroy()


	def change_colour(self, colour: str):
		"""
		method changes the current active draw colour on the canvas
		:param new_colour: str
		:return: None
		"""
		self.drawing_colour = colour


	def build_palette(self):
		"""
		method draws the available palette of colours to the canvas
		:return: None
		"""
		id = self.active_canvas.create_rectangle((10, 10, 30, 30), fill='black')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('black'))
		
		id = self.active_canvas.create_rectangle((10, 40, 30, 60), fill='grey')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('grey'))
		
		id = self.active_canvas.create_rectangle((10, 70, 30, 90), fill='brown')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('brown'))
		
		id = self.active_canvas.create_rectangle((10, 100, 30, 120), fill='red')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('red'))
		
		id = self.active_canvas.create_rectangle((10, 130, 30, 150), fill='orange')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('orange'))
		
		id = self.active_canvas.create_rectangle((10, 160, 30, 180), fill='yellow')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('yellow'))
		
		id = self.active_canvas.create_rectangle((10, 190, 30, 210), fill='green')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('green'))
		
		id = self.active_canvas.create_rectangle((10, 220, 30, 240), fill='blue')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('blue'))
		
		id = self.active_canvas.create_rectangle((10, 250, 30, 270), fill='purple')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('purple'))


	def locate_xy(self, event: object):
		"""
		method locates the current x, y position of the cursor
		:param event: object
		:return: None
		"""
		self.current_x, self.current_y = (event.x, event.y)
		print(f'({self.current_x}, {self.current_y})')


	def draw_line(self, event: object):
		"""
		method draws a line to self.active_canvas
		:param event: object
		:return: None
		"""
		print(f'({self.current_x}, {self.current_y}), ({event.x}, {event.y})')
		self.active_canvas.create_line(
			(self.current_x, self.current_y, event.x, event.y),
			fill=self.drawing_colour
		)
		self.current_x, self.current_y = (event.x, event.y)


	def new_whiteboard(self):
		"""
		method clears the canvas
		:return: None
		"""
		self.active_canvas.delete('all')
		self.build_palette()


	def build(self):
		"""
		method builds the application
		:return: None
		"""
		self.geometry("600x360")
		self.configure(bg='white')
		self.resizable(False, False)
		self.title("Whiteboard")
		
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

		menubar = Menu(master=self, bg='white')
		self.config(menu=menubar)
		submenu = Menu(menubar, tearoff=0)

		menubar.add_cascade(label='File', menu=submenu)
		submenu.add_command(label='New Whiteboard', command=self.new_whiteboard)
		submenu.add_command(label='Save Whiteboard', command=lambda: print(NotImplemented))

		self.active_canvas = Canvas(master=self, bg='white')
		self.active_canvas.grid(row=0, column=0, sticky='nsew')

		self.active_canvas.bind('<Button-1>', self.locate_xy)
		self.active_canvas.bind('<B1-Motion>', self.draw_line)

		self.build_palette()

		self.protocol("WM_DELETE_WINDOW", self.close_window)

		self.mainloop()