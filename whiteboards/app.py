# absolute imports
import os
from tkinter import Tk, Toplevel, Canvas, PhotoImage, Entry, Button, messagebox
from guizero import App

# relative imports
from .whiteboard import WhiteboardInstance
from .security.authentication import Authenticator

'''
for now a valid user is: {username = "test", password = "test"}
'''


class WhiteboardApp(Tk):
	def __init__(self, base_widget: App = None):
		super().__init__()
		self.authenticator = Authenticator()
		self.authenticator.decrypt_dataframe()

		self.assets_path = os.path.join('whiteboards', 'assets')

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
		state = self.authenticator.authenticate(att_user, att_pass)
		if state:
			whiteboard = WhiteboardInstance(instantiator=self)
			whiteboard()
		else:
			messagebox.showwarning(title='Error', message="Failed to login!", parent=canvas)


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
		self.signup_win.resizable(False, False)
		self.signup_win.title("Sign up")

		self.signup_win.protocol("WM_DELETE_WINDOW", self.close_signup)


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
			file=os.path.join(self.assets_path, 'entry_box.png')
		)
		canvas.create_image(388.0, 241.5, image=username_box_img)
		username_box = Entry(master=canvas, bd=0, bg='#e3e3e3', highlightthickness=0)
		username_box.place(x=329, y=230, width=118, height=21)

		password_box_img = PhotoImage(
			master=canvas,
			file=os.path.join(self.assets_path, 'entry_box.png')
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
			file=os.path.join(self.assets_path, 'login_button.png')
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
			file=os.path.join(self.assets_path, 'signup_button.png')
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
			file=os.path.join(self.assets_path, 'background.png')
		)
		canvas.create_image(229, 189.5, image=background_img)

		self.protocol("WM_DELETE_WINDOW", self.close_app)

		self.mainloop()
