from PIL import Image
from typing import Any, Dict, List, Literal, Optional, Tuple, Union, TYPE_CHECKING
import customtkinter as ctk
from tkinter import Event, Text, Entry, Widget, messagebox
import sendrequests
from websockets.sync.client import connect
from websockets.exceptions import ConnectionClosed
from threading import Thread
from json import loads
from base64 import b64decode
from io import BytesIO
import os
from dotenv import load_dotenv
from config import Settings
from savemessages import Writer

if TYPE_CHECKING:
	from config import Settings

load_dotenv("config.env")

WS = 'wss://fun.guimx.me/ws/'

class Chat(ctk.CTk):
	def __init__(self, width: int, height: int, token: str, user_name: str):
		super().__init__()
		self.title('Java Connect')
		self.user_name = user_name
		self._bg_color = os.getenv("BACKGROUND_COLOR")
		self._text_input_color = os.getenv("INPUT_BAR_COLOR")
		self._bubble_text_color = os.getenv("TEXT_BUBBLE_COLOR")
		self._message_text_color = os.getenv("TEXT_COLOR")

		self.CONTACT_FONT = ctk.CTkFont(family='Arial', size=20, weight='bold')
		self.iconbitmap('assets\\logo.ico')
		self.width = width
		self.height = height
		self._token = token
		self.resizable(False, False)
		self.geometry(self.center_window_to_display(self, width, height))
		self._enable_widgets()
		self.bind('<Key>',lambda event: self.on_key_press(event))
		self.current_contact: Optional[str] = None
		self.messages: List[Dict[str,Union[ctk.CTkLabel,str,Dict[str,Any]]]] = []
		self.get_messages(token)
		self.rate_limited = False
		self.pending_messages = []
		self._custom_settings: Optional['Settings'] = None

		self.load_messages()

	@property
	def token(self):
		return self._token
	@token.setter
	def token(self, value: str):
		self._token = value

	@property
	def bg_color(self):
		return self._bg_color
	@bg_color.setter
	def bg_color(self, value: str):
		self._bg_color = value
		self.frame.configure(fg_color=self._bg_color)
		self.contact_frame.configure(fg_color=self._bg_color,scrollbar_fg_color=self._bg_color)
	@property
	def text_input_color(self):
		return self._text_input_color
	@text_input_color.setter
	def text_input_color(self, value: str):
		self._text_input_color = value
		self.text_input.configure(fg_color=self._text_input_color)
	@property
	def bubble_text_color(self):
		return self._bubble_text_color
	@bubble_text_color.setter
	def bubble_text_color(self, value: str):
		self._bubble_text_color = value
	@property
	def message_text_color(self):
		return self._message_text_color
	@message_text_color.setter
	def message_text_color(self, value: str):
		self._message_text_color = value

	def get_messages(self, token: str):
		def listen():
			with connect(WS) as websocket:
				websocket.send(token)
				auth_response = websocket.recv()
				print(auth_response)
				try:
					while True:
						response = websocket.recv()
						if isinstance(response,str):
							info = loads(response)
							file = info.get('file',None)
							if file is not None:
								file = b64decode(file)
							info['file'] = file
							info['is_self'] = False
							self.write_message(info['message'],file,info['sender'],False)
							if self.current_contact is not None and info['sender'] == self.current_contact:
								self.spawn_message('w',info['message'],
						   			file)
								#TODO: Add download file support + remove trying to display a file that isn't an image
							else:
								self.pending_messages.append(info)
				except ConnectionClosed:
					print(f"Connection closed.")
					exit(0)
		Thread(target=listen,daemon=True).start()

	def load_messages(self):
		with Writer() as writer:
			writer.create_table()
			messages = writer.load_all()
		for message in messages:
			self.pending_messages.append({'sender':message.contact,'message':message.message,'file':message.file,'is_self':message.is_self})


	@staticmethod
	def center_window_to_display(screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0) -> str:
		screen_width = screen.winfo_screenwidth()
		screen_height = screen.winfo_screenheight()
		x = int((screen_width/2) - (width/2) * scale_factor)
		y = int((screen_height/2) - (height/2) * scale_factor)
		return f'{width}x{height}+{x}+{y}'

	@property
	def custom_settings(self):
		return self._custom_settings
	
	@custom_settings.setter
	def custom_settings(self, value: Optional['Settings']):
		self._custom_settings = value

	def setings_button_callback(self):
		self.withdraw()
		if self._custom_settings is None or self._custom_settings.winfo_exists():
			self._custom_settings = Settings(960,610,self,self.user_name)
		else:
			self._custom_settings.focus()


	def _enable_widgets(self):
		
		self.send_button = ctk.CTkButton(self,text='',command=lambda : Thread(target=self.spawn_message,daemon=True).start(),
								   image=ctk.CTkImage(Image.open('assets\\send.png'),size=(30,30)),
								   width=30,height=30)
		self.send_button.configure(fg_color='transparent',hover_color='#555555')
		self.attachment_button = ctk.CTkButton(self,text='',
									image=ctk.CTkImage(Image.open('assets\\clip.png'),size=(25,25)),
									width=30,height=30,command=self.open_attachment)
		self.attachment_button.configure(fg_color='transparent',hover_color='#555555')
		self.frame = ctk.CTkScrollableFrame(self,fg_color=self.bg_color,orientation='vertical',
				width=int(self.width*0.60), height=self.height-80)
		self.text_input = ctk.CTkTextbox(self,fg_color=self.text_input_color,width=int(self.width*0.60)-80, height=35)

		self.contact_frame = ctk.CTkScrollableFrame(self,fg_color=self.bg_color,orientation='vertical',
				width=int(self.width*0.35), height=self.height-35,scrollbar_fg_color=self.bg_color,scrollbar_button_color=self.bg_color,
				scrollbar_button_hover_color='#242424')
		self.contact_frame.grid_columnconfigure(0, weight=1)
		self.contact_frame.grid_columnconfigure(1, weight=0)
		self.contact_frame.place(anchor='nw',x=10,y=10)
		self.add_entry = ctk.CTkEntry(self.contact_frame,fg_color='#242424',width=int(self.width*0.31),corner_radius=10)
		self.add_entry.grid(row=0,column=0,sticky='w')
		self.add_button = ctk.CTkButton(self.contact_frame,text='',command=self.add_contact,corner_radius=10,
								  image=ctk.CTkImage(Image.open('assets\\add.png'),size=(30,30)),width=30,height=30)
		self.add_button.configure(fg_color='transparent',hover_color='#555555')
		self.add_button.grid(row=0,column=1,sticky='e')

		self.settings_button = ctk.CTkButton(self.contact_frame,text='',command= self.setings_button_callback,
									   image=ctk.CTkImage(Image.open('assets\\settings.png'),size=(30,30)),width=30,height=30)
		self.settings_button.configure(fg_color='transparent',hover_color='#555555')
		
	def write_message(self, message: Optional[str], file: Optional[bytes], contact: str, is_self: bool):
		with Writer() as writer:
			writer.write(message, file, contact, is_self)

	def add_contact(self):
		if not self.add_entry.get().strip() or self.current_contact is not None and self.current_contact == self.add_entry.get(): return
		try:
			data = sendrequests.load_other_pfp(self.add_entry.get())
		except sendrequests.BaseException as e:
			messagebox.showerror('Error', str(e))
			return
		contact = ctk.CTkButton(self.contact_frame,text=self.add_entry.get(),fg_color='#242424',hover_color='#555555',anchor='w',
						  height=70,image=ctk.CTkImage(Image.open(BytesIO(data)),size=(50,50)),compound='left')
		contact.bind('<Button-1>',lambda e: self.contact_button_clicked(contact.cget('text')))
		contact.configure(font=self.CONTACT_FONT)
		contact.grid(row=len(self.contact_frame.children), column=0, sticky='we',pady=(20, 10))
		separator_line = ctk.CTkCanvas(self.contact_frame, height=1, bg='#555555', highlightthickness=0)
		separator_line.grid(row=len(self.contact_frame.children), column=0, sticky='we', pady=(20, 10))

	def spawn_message(self, sticky: Literal['e','w'] = 'e', message: Optional[str] = None, attachment: Optional[bytes] = None):
		#'e' para derecha, 'w' para izquierda
		if self.current_contact is None:
			return
		color = self.bubble_text_color
		if not message:
			message = self.text_input.get('1.0', 'end').strip()
			self.text_input.delete('1.0', 'end')
			if sticky == 'e':
				if not message.strip() and not attachment:
					return
				try:
					data = sendrequests.send_message(self.token,self.current_contact,message,attachment)
					self.rate_limited = False
					with Writer() as writer:
						writer.write(message,attachment,self.current_contact,True)
				except sendrequests.RateLimited as e:
					color = 'red'
					if not self.rate_limited:
						self.rate_limited = True
						messagebox.showerror(f'Error', str(e))
						self.rate_limited = False
		message_box = ctk.CTkLabel(self.frame,width=200,text=message,text_color=self.message_text_color,fg_color=color if sticky == 'e' else '#3C3C3C',
					corner_radius=20,anchor='ne',padx=0, pady=20,wraplength=500)
		if attachment is not None: message_box.configure(image=ctk.CTkImage(Image.open(BytesIO(attachment)),size=(200,200)),compound='bottom')
		message_box.configure(height=message_box.winfo_reqheight()+28) #For some reason text in label f*cks up the height and it looks bad
		message_box.grid(row=len(self.messages)+1, column=0, sticky=sticky,pady=(20, 0))
		self.frame._parent_canvas.update_idletasks()
		self.frame._parent_canvas.config(scrollregion=self.frame._parent_canvas.bbox("all"))
		self.frame._parent_canvas.yview_moveto(1.0)
		self.messages.append({'recipient':self.current_contact,'widgets':message_box,'grid_info':message_box.grid_info()}) #type: ignore

	def on_key_press(self, event: Event):
		if event.keysym == "Return":
			self.spawn_message()
		elif not isinstance(self.text_input.focus_get(),(Text,Entry)) and self.text_input.winfo_ismapped():
			self.text_input.focus_set()
			self.text_input.insert('end',event.char)

	def contact_button_clicked(self, text: str):
		self.current_contact = text
		if not self.frame.winfo_ismapped():
			self.frame.grid_columnconfigure(0, weight=1)
			self.frame.grid_columnconfigure(1, weight=0)
			self.frame.place(anchor='ne',x=self.width-10,y=10)
			self.text_input.place(anchor='se',x=self.width-115,y=self.height-10)
			self.send_button.place(anchor='se',x=self.width-10,y=self.height-10)
			self.attachment_button.place(anchor='se',x=self.width-60,y=self.height-11) #bruh
			self.settings_button.grid(row=0,column=2,sticky='e')
		else:
			for widget in self.frame.winfo_children():
				widget.grid_forget()
			for message in self.messages:
				if message['recipient'] == text:
					message['widgets'].grid(**message['grid_info']) #type: ignore
		for pending_message in self.pending_messages.copy():
			if pending_message['sender'] == text:
				is_self = pending_message.get('is_self',False)
				self.spawn_message('e' if is_self else 'w',pending_message['message'],pending_message.get('file',None))
				self.pending_messages.remove(pending_message)

	def open_attachment(self):
		file = ctk.filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;")])
		if file:
			with open(file,'rb') as f:
				self.spawn_message('e',attachment=f.read())

	def _test_widget_change(self):
		#This has no real use, just to test changing widgets
		saved_widgets: List[Tuple[Widget,Dict[str,Any]]] = []

		for widget in self.frame.winfo_children():
			saved_widgets.append((widget,widget.grid_info())) #type: ignore
			widget.grid_forget()
	
		for widget,grid_info in saved_widgets:
			widget.configure(fg_color="red")  #type: ignore
			widget.grid(**grid_info)


