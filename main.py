import customtkinter as ctk
from tkinter import messagebox
import sendrequests
from PIL import Image
from typing import Dict, Any

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
		self.title('JustConnect')
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
			Register(1200,800).mainloop()

	def _enable_widgets(self):
		self.white_left = ctk.CTkLabel(self,text='',bg_color='#EEEFF0',width=400,height=800)
		self.white_left.place(anchor='nw')

		self.logo = ctk.CTkImage(Image.open('assets\\logo.ico'),size=(45,45))
		self.logo_label = ctk.CTkLabel(self,image=self.logo,text='')
		self.logo_label.place(anchor='ne',relx=0.72,rely=0.1)

		self.jc_label = ctk.CTkLabel(self,text="JAVACONNECT",font=self.font_subtitle,width=125)
		self.jc_label.place(anchor='e',relx=0.89,rely=0.13)
		self.jc_label.place

		self.main_logo = ctk.CTkImage(Image.open('assets\\j.png'),size=(400,400))
		self.main_logo_label = ctk.CTkLabel(self,image=self.main_logo,text='')
		self.main_logo_label.place(anchor='w',relx=0.0,rely=0.5)

		self.login_label = ctk.CTkLabel(self,text=('INICIAR SESIÓN'), width = 30, height = 50,font=self.font_title,padx=30)
		self.login_label.place(anchor='center', relx=0.5, rely=0.25)
		# login_label.place(anchor='e',relx=0.9,rely=0.3)


		self.username_label = ctk.CTkLabel(self,text=('Usuario'), width = 30, height = 50,font=self.font_subtitle,pady=10)
		self.username_label.place(anchor='center', relx=0.5, rely=0.4)


		self.login_text = ctk.CTkEntry(self,height=30, width=300,font=self.font_subtitle)
		self.login_text.place(anchor='center', relx=0.5, rely=0.5)
		# login_text.place(anchor = 'e',relx=0.9,rely=0.4)

		self.passwd_label = ctk.CTkLabel(self,text=('Contraseña'), width = 30, height = 50,font=self.font_subtitle,pady=10)
		self.passwd_label.place(anchor='center', relx=0.5, rely=0.6)

		self.passwd_text = ctk.CTkEntry(self,height=30,width=300,show='*',font=self.font_subtitle)
		self.passwd_text.place(anchor='center', relx=0.5, rely=0.7)
		# passwd_text.place(anchor = 'e',relx=0.9,rely=0.5)


		self.button = ctk.CTkButton(self, text='Log-in', command = self._button_callback,width=300,height=35)
		self.button.place(anchor='center', relx=0.5, rely=0.8)

class Register(Login):
	def __init__(self, width: int, height: int):
		super().__init__(width, height)
		self.login_label.configure(text='REGISTRO')
		self.button.configure(text='Registrarse')

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
			Login(1200,800).mainloop()

login = Login(1200,800)
login.mainloop()