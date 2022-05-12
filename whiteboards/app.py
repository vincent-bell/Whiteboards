# absolute imports
import os
from tkinter import Tk, Toplevel, Canvas, PhotoImage, Entry, Button, messagebox
from guizero import App

# relative imports
from .whiteboard import WhiteboardInstance
from .security.authentication import Authenticator


class WhiteboardApp(Tk):
	def __init__(self, base_widget: App = None):
		super().__init__()
		self.authenticator = Authenticator()
		self.authenticator.decrypt_dataframe()
		
		self.assets_path_init = os.path.join('whiteboards', 'assets', 'init')
		self.assets_path_signup = os.path.join('whiteboards', 'assets', 'sign_up')

		if base_widget:
			self.base_widget = base_widget
			self.base_widget.disable()
		else:
			self.base_widget = None


	def __call__(self):
		"""
		method calls self.build when a WhiteboardApp object is called
		:return: None
		"""
		self.build()


	def close_app(self) -> None:
		"""
		method to call when window is closed
		:return: None
		"""
		if self.base_widget:
			self.base_widget.enable()
		self.destroy()


	def close_signup(self):
		"""
		method to call when sign up window is closed
		:return: None
		"""
		self.login_button['state'] = "normal"
		self.signup_button['state'] = "normal"
		self.signup_win.destroy()


	def click_login(self, att_user: str, att_pass: str, canvas):
		"""
		method attempts to authenticate a user when the 'Login' button is pressed
		if user authentication is successful then this method will create a new
		whiteboard instance
		:param att_user: str
		:param att_pass: str
		:param canvas: object
		:return: None
		"""
		state = self.authenticator.authenticate(username=att_user, password=att_pass)
		if state:
			whiteboard = WhiteboardInstance(instantiator=self)
			whiteboard()
		else:
			messagebox.showwarning(title='Error', message="Failed to login!", parent=canvas)


	def click_signup_2(self, try_username: str, try_pass: str, try_pass_conf:str, canvas:str):
		state, e_type = self.authenticator.sign_up(username=try_username, password=try_pass, password_conf=try_pass_conf)
		if state and not e_type:
			# display that the user signed up successfully and gracefully close the sign-up window
			self.close_signup()
		else:
			if e_type == 'INV_USER_LEN':
				messagebox.showwarning(title='Error', message="Username must be at least 8 characters!", parent=canvas)
			elif e_type == 'ALPHABET_E':
				messagebox.showwarning(title='Error', message="Username can only contain characters in the english alphabet!", parent=canvas)
			elif e_type == 'A_EXIST':
				messagebox.showwarning(title='Error', message="Username already exists!", parent=canvas)
			elif e_type == 'INV_PASS_LEN':
				messagebox.showwarning(title='Error', message="Password must be at least 8 characters!", parent=canvas)
			elif e_type == 'PASS_NE':
				messagebox.showwarning(title='Error', message="The passwords do not match!", parent=canvas)


	def click_signup(self):
		"""
		method creates a sign up window to allow for new account creation
		:return: None
		"""
		WIDTH, HEIGHT = 250, 300
		self.login_button['state'] = "disabled"
		self.signup_button['state'] = "disabled"
		self.signup_win = Toplevel()
		self.signup_win.geometry("{}x{}".format(WIDTH, HEIGHT))
		self.signup_win.configure(bg='white')
		self.signup_win.resizable(False, False)
		self.signup_win.title("Sign up")

		canvas = Canvas(
			self.signup_win,
			bg='white',
			height=300,
			width=250,
			bd=0,
			highlightthickness=0,
			relief='ridge'
		)
		canvas.place(x=0, y=0)

		username_box_img = PhotoImage(
			master=canvas,
			file=os.path.join(self.assets_path_signup, 'entry_box.png')
		)
		canvas.create_image(163.5, 147, image=username_box_img)
		username_box = Entry(master=canvas, bd=0, bg='#E3E3E3', highlightthickness=0)
		username_box.place(x=111, y=138, width=105, height=16)

		password_box_img = PhotoImage(
			master=canvas,
			file=os.path.join(self.assets_path_signup, 'entry_box.png')
		)
		canvas.create_image(163.5, 230, image=password_box_img)
		password_box = Entry(master=canvas, bd=0, bg='#E3E3E3', highlightthickness=0, show='*')
		password_box.place(x=111, y=221, width=105, height=16)

		confirm_password_box_img = PhotoImage(
			master=canvas,
			file=os.path.join(self.assets_path_signup, 'entry_box.png')
		)
		canvas.create_image(163.5, 187, image=confirm_password_box_img)
		confirm_password_box = Entry(master=canvas, bd=0, bg='#E3E3E3', highlightthickness=0, show='*')
		confirm_password_box.place(x=111, y=178, width=105, height=16)

		signup_button_img = PhotoImage(
				master=canvas,
				file=os.path.join(self.assets_path_signup, 'signup_button.png')
		)
		signup_button = Button(
			master=canvas,
			image=signup_button_img,
			borderwidth=0,
			highlightthickness=0,
			command=lambda: self.click_signup_2(
				try_username=username_box.get(), 
				try_pass=confirm_password_box.get(),
				try_pass_conf=password_box.get(),
				canvas=canvas
			),
			relief='flat'
		)
		signup_button.place(x=128, y=257, width=65, height=25)

		background_img = PhotoImage(
			master=canvas,
			file=os.path.join(self.assets_path_signup, 'background.png')
		)
		canvas.create_image(138.5, 137.5, image=background_img)

		self.signup_win.protocol("WM_DELETE_WINDOW", self.close_signup)

		self.signup_win.mainloop()


	def build(self):
		"""
		method builds the application
		:return: None
		"""
		self.geometry("500x380")
		self.configure(bg='white')
		self.resizable(False, False)
		self.title("Whiteboard App")

		canvas = Canvas(
		    self,
		    bg = 'white',
		    height = 380,
		    width = 500,
		    bd = 0,
		    highlightthickness = 0,
		    relief = "ridge")
		canvas.place(x = 0, y = 0)

		username_box_img = PhotoImage(
			master=canvas,
			file=os.path.join(self.assets_path_init, 'entry_box.png')
		)
		canvas.create_image(388.0, 241.5, image=username_box_img)
		username_box = Entry(master=canvas, bd=0, bg='#e3e3e3', highlightthickness=0)
		username_box.place(x=329, y=230, width=118, height=21)

		password_box_img = PhotoImage(
			master=canvas,
			file=os.path.join(self.assets_path_init, 'entry_box.png')
		)
		canvas.create_image(388, 301.5, image=password_box_img)
		password_box = Entry(
			master=canvas,
			bd=0,
			bg='#e3e3e3',
			highlightthickness=0,
			show='*'
		)
		password_box.place(x=329, y=290, width=118, height=21)

		login_button_img = PhotoImage(
			master=canvas,
			file=os.path.join(self.assets_path_init, 'login_button.png')
		)
		self.login_button = Button(
			master=canvas,
			image=login_button_img,
			borderwidth = 0,
    		highlightthickness = 0,
    		command = lambda: self.click_login(
				att_user=username_box.get(),
				att_pass=password_box.get(),
				canvas=canvas
			)
		)
		self.login_button.place(x=316, y=333, width=70, height=32)

		signup_button_img = PhotoImage(
			master=canvas,
			file=os.path.join(self.assets_path_init, 'signup_button.png')
		)
		self.signup_button = Button(
			master=canvas,
			image=signup_button_img,
			borderwidth = 0,
    		highlightthickness = 0,
    		command = self.click_signup,
    		relief = "flat"
		)
		self.signup_button.place(x=393, y=333, width=69, height=32)

		background_img = PhotoImage(
			master=canvas,
			file=os.path.join(self.assets_path_init, 'background.png')
		)
		canvas.create_image(229, 189.5, image=background_img)

		self.protocol("WM_DELETE_WINDOW", self.close_app)

		self.mainloop()

