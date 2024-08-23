import customtkinter as ctk
from tkinter import messagebox
import sendrequests
from PIL import Image
from typing import Dict, Any
from chat import Chat

def center_window_to_display(screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0) -> str:
	screen_width = screen.winfo_screenwidth()
	screen_height = screen.winfo_screenheight()
	x = int((screen_width/2) - (width/2) * scale_factor)
	y = int((screen_height/2) - (height/2) * scale_factor)
	return f'{width}x{height}+{x}+{y}'

class Login(ctk.CTk):
	
	def __init__(self, width: int, height: int):
		super().__init__()
		self.font_subtitle = ctk.CTkFont('SegoeUi',size=20,weight='bold')
		self.font_title = ctk.CTkFont('SegoeUi',size=35,weight='bold')
		self.title('Java Connect')
		self.geometry(center_window_to_display(self, width, height))
		self.resizable(False, False)
		self.iconbitmap('assets\\logo.ico')
		self.configure(foreground='#16181D')
		self.bind('<Return>',lambda event: self._button_callback())
		self._enable_widgets()	
	
	def _button_callback(self):
		user = self.login_text.get()
		passwd = self.passwd_text.get()
		if not user.replace(' ','') or not passwd.replace(' ',''):
			messagebox.showerror('Error', 'No puedes dejar campos vacíos')
			return
		try:
			data: Dict[str,Any] = sendrequests.login(user, passwd)
		except sendrequests.BaseException as e:
			messagebox.showerror('Error', str(e))
			self.passwd_text.delete(0, 'end')
		else:
			self.destroy()
			Chat(1800,800).mainloop()

	def _enable_widgets(self):
		self.white_left = ctk.CTkLabel(self,text='',bg_color='#EEEFF0',width=283,height=610)
		self.white_left.place(anchor='nw')

		self.logo = ctk.CTkImage(Image.open('assets\\logo.ico'),size=(35,35))
		self.logo_label = ctk.CTkLabel(self,image=self.logo,text='')
		self.logo_label.place(anchor='center',relx=0.72,rely=0.25)

		self.jc_label = ctk.CTkLabel(self,text="Java Connect",font=self.font_subtitle,width=125)
		self.jc_label.place(anchor='e',relx=0.88,rely=0.25)
		self.jc_label.place

		self.main_logo = ctk.CTkImage(Image.open('assets\\j.png'),size=(283,283))
		self.main_logo_label = ctk.CTkLabel(self,image=self.main_logo,text='')
		self.main_logo_label.place(anchor='w',relx=0.0,rely=0.5)

		self.login_label = ctk.CTkLabel(self,text=('INICIAR SESIÓN'), width = 30, height = 50,font=self.font_title,padx=30)
		self.login_label.place(anchor='center', relx=0.5, rely=0.25)
		# login_label.place(anchor='e',relx=0.9,rely=0.3)


		self.username_label = ctk.CTkLabel(self,text=('Usuario'), width = 30, height = 50,font=self.font_subtitle,pady=10)
		self.username_label.place(anchor='e', relx=0.44, rely=0.38)


		self.login_text = ctk.CTkEntry(self,height=30, width=273,font=self.font_subtitle,fg_color='#242424',border_color='#242424',placeholder_text='Nombre de usuario')
		self.login_text.place(anchor='center', relx=0.5, rely=0.46)
		# login_text.place(anchor = 'e',relx=0.9,rely=0.4)


		self.passwd_label = ctk.CTkLabel(self,text=('Contraseña'), width = 30, height = 50,font=self.font_subtitle,pady=10)
		self.passwd_label.place(anchor='center', relx=0.42, rely=0.54)


		self.passwd_text = ctk.CTkEntry(self,height=30,width=273,show='*',font=self.font_subtitle,fg_color='#242424',border_color='#242424',placeholder_text='*******')
		self.passwd_text.place(anchor='center', relx=0.5, rely=0.6)
		# passwd_text.place(anchor = 'e',relx=0.9,rely=0.5)


		self.button = ctk.CTkButton(self, text='Log-in', command = self._button_callback,width=273,height=35,fg_color='#eeeff0',hover_color='#3D3D3D',text_color='#242424')
		self.button.place(anchor='center', relx=0.5, rely=0.68)


		self.register_label = ctk.CTkLabel(self, text='¿No tienes una cuenta?', font=self.font_subtitle)
		self.register_label.place(anchor='center', relx=0.43, rely=0.95)
		self.register_button = ctk.CTkButton(self, text='Registrate', command=self.open_register_form, width=35, height=35,fg_color='#242424',hover_color='#3D3D3D')
		self.register_button.place(anchor='center', relx=0.58, rely=0.95)

	def open_register_form(self):
			self.destroy()
			Register(981,610).mainloop()

class Register(Login):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.login_label.configure(text='REGISTRO')
		self.button.configure(text='Registrarse')
		self.register_button.configure(text='Log-in', command=self.open_login_form)
		self.register_label.configure(text='¿Ya tienes una cuenta?')
	
	def _button_callback(self):
		user = self.login_text.get()
		passwd = self.passwd_text.get()
		if not user.replace(' ','') or not passwd.replace(' ',''):
			messagebox.showerror('Error', 'No puedes dejar campos vacíos')
			return
		try:
			data: Dict[str,Any] = sendrequests.register(user, passwd)
		except sendrequests.BaseException as e:
			messagebox.showerror('Error', str(e))
			self.passwd_text.delete(0, 'end')
		else:
			self.destroy()
			Chat(1800,800).mainloop()

	def open_login_form(self):
		self.destroy()
		Login(981,610).mainloop()
	
login = Login(981,610)
login.mainloop()