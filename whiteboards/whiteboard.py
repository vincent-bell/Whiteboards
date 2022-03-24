from tkinter import Tk, Canvas, Menu
from tkinter.filedialog import asksaveasfile


class WhiteboardInstance(Tk):
	state = 'drawing' # default state
	
	def __init__(self, instantiator):
		super().__init__()
		self.instantiator = instantiator
		self.instantiator.destroy()

		self.current_x, self.current_y = (0,0)
		self.drawing_colour = 'black'

		self.next_unbind = None


	def __call__(self):
		"""
		This method calls self.build when a WhiteboardInstance object is called.
		:return: None
		"""
		self.build()


	def close_window(self):
		"""
		The method to call when whiteboard window is closed.
		:return: None
		"""
		if self.instantiator.base_widget:
			self.instantiator.base_widget.enable()
		self.destroy()


	def change_colour(self, colour: str):
		"""
		This method changes the current active colour on the canvas.
		:param new_colour: str
		:return: None
		"""
		self.drawing_colour = colour


	def build_palette(self):
		"""
		This method draws the available palette of colours to the canvas.
		:return: None
		"""
		id = self.active_canvas.create_rectangle((10, 40, 30, 60), fill='black')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('black'))
		
		id = self.active_canvas.create_rectangle((10, 70, 30, 90), fill='grey')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('grey'))
		
		id = self.active_canvas.create_rectangle((10, 100, 30, 120), fill='brown')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('brown'))
		
		id = self.active_canvas.create_rectangle((10, 130, 30, 150), fill='red')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('red'))
		
		id = self.active_canvas.create_rectangle((10, 160, 30, 180), fill='orange')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('orange'))
		
		id = self.active_canvas.create_rectangle((10, 190, 30, 210), fill='yellow')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('yellow'))
		
		id = self.active_canvas.create_rectangle((10, 220, 30, 240), fill='green')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('green'))
		
		id = self.active_canvas.create_rectangle((10, 250, 30, 270), fill='blue')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('blue'))
		
		id = self.active_canvas.create_rectangle((10, 280, 30, 300), fill='purple')
		self.active_canvas.tag_bind(id, '<Button-1>', lambda colour: self.change_colour('purple'))


	def build_tools(self):
		"""
		This method builds the tools to the right of the whiteboard:
		Pen, Paint Brush, Create-Circle, Sticky Notes which should be
		images bound to tags on the self.active_canvas object.
		"""
		# to the right of the screen
		NotImplemented


	def locate_xy(self, event: object):
		"""
		This method locates the current x, y position of the cursor.
		:param event: object
		:return: None
		"""
		self.current_x, self.current_y = (event.x, event.y)
		print(f'({self.current_x}, {self.current_y})')


	def draw_line(self, event: object):
		"""
		This method draws a line to self.active_canvas based on cursor pos.
		:param event: object
		:return: None
		"""
		print(f'({self.current_x}, {self.current_y}), ({event.x}, {event.y})')
		self.active_canvas.create_line(
			(self.current_x, self.current_y, event.x, event.y),
			fill=self.drawing_colour
		)
		self.current_x, self.current_y = (event.x, event.y)


	def draw_oval(self, event: object):
		"""
		This method draws an oval to self.active_canvas based on cursor pos.
		:param event: object
		:return: None
		"""
		self.active_canvas.create_oval(
			(self.current_x, self.current_y, event.x, event.y),
			outline=self.drawing_colour
		)
		self.current_x, self.current_y = (event.x, event.y)


	def new_whiteboard(self):
		"""
		This method clears the canvas and re-draws the available colour palette.
		:return: None
		"""
		self.active_canvas.delete('all')
		self.build_palette()


	def save_whiteboard(self):
		"""
		This method allows a user to save a whiteboard state as a png image
		:return: None
		"""
		whiteboard_image = None
		# somehow obtain a jpg/png image of the whiteboard in bytes format in a variable
		# maybe PIL or ImageMagik?
		file = asksaveasfile(
			mode='wb',
			initialfile='Untitled.png',
			defaultextension=".png",
			filetypes=[("All Files", "*.*"), ("Png Image", "*.png")]
		)
		file.write(whiteboard_image)
		print(file)

		file.close()


	def switch_bindings(self):
		"""
		This method switches the canvas key bindings based on the draw state of WhiteboardInstance.
		:return: None
		"""
		if self.next_unbind == 'drawing':
			self.active_canvas.unbind('<B1-Motion>')
		elif self.next_unbind == 'create-circle':
			self.active_canvas.unbind('<ButtonRelease-1>')

		if WhiteboardInstance.state == 'drawing':
			self.active_canvas.bind('<B1-Motion>', self.draw_line)
			self.next_unbind = 'drawing'
		elif WhiteboardInstance.state == 'create-circle':
			self.active_canvas.bind('<ButtonRelease-1>', self.draw_oval)
			self.next_unbind = 'create-circle'


	def build(self):
		"""
		This method builds the application.
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
		submenu.add_command(label='Save Whiteboard', command=self.save_whiteboard)

		self.active_canvas = Canvas(master=self, bg='white')
		self.active_canvas.grid(row=0, column=0, sticky='nsew')
        
		self.active_canvas.bind('<Button-1>', lambda event: [
			self.locate_xy(event),
			self.switch_bindings()
		])

		self.build_palette()

		self.protocol("WM_DELETE_WINDOW", self.close_window)

		self.mainloop()
