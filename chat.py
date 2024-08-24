from PIL import Image
from typing import Any, Dict, List, Literal, Optional, Tuple, Union
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

load_dotenv("config.env")

WS = 'wss://fun.guimx.me/ws/'

class Chat(ctk.CTk):
	def __init__(self, width: int, height: int, token: str, color: str = '#242424'):
		super().__init__(fg_color=color)		
		self.CONTACT_FONT = ctk.CTkFont(family='Arial', size=20, weight='bold')
		self.width = width
		self.height = height
		self.token = token
		self.resizable(False, False)
		self.geometry(self.center_window_to_display(self, width, height))
		self._enable_widgets()
		self.bind('<Key>',lambda event: self.on_key_press(event))
		self.current_contact: Optional[str] = None
		self.messages: List[Dict[str,Union[ctk.CTkLabel,str,Dict[str,Any]]]] = []
		self.get_messages(token)
		self.rate_limited = False
		self.pending_messages = []

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
							if self.current_contact is not None and info['sender'] == self.current_contact:
								file = info.get('file',None)
								self.spawn_message('w',info['message'],
						   			b64decode(file) if file is not None else None)
								#TODO: Add download file support + remove trying to display a file that isn't an image
							else:
								self.pending_messages.append(info)
				except ConnectionClosed:
					print(f"Connection closed.")
					exit(0)
		Thread(target=listen,daemon=True).start()

	@staticmethod
	def center_window_to_display(screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0) -> str:
		screen_width = screen.winfo_screenwidth()
		screen_height = screen.winfo_screenheight()
		x = int((screen_width/2) - (width/2) * scale_factor)
		y = int((screen_height/2) - (height/2) * scale_factor)
		return f'{width}x{height}+{x}+{y}'

	def _enable_widgets(self):
		self.send_button = ctk.CTkButton(self,text='',command=lambda : Thread(target=self.spawn_message,daemon=True).start(),
								   image=ctk.CTkImage(Image.open('assets\\send.png'),size=(30,30)),
								   width=30,height=30)
		self.send_button.configure(fg_color='transparent',hover_color='#555555')
		self.attachment_button = ctk.CTkButton(self,text='',
									image=ctk.CTkImage(Image.open('assets\\clip.png'),size=(25,25)),
									width=30,height=30,command=self.open_attachment)
		self.attachment_button.configure(fg_color='transparent',hover_color='#555555')
		self.frame = ctk.CTkScrollableFrame(self,fg_color=os.getenv("BACKGROUND_COLOR"),orientation='vertical',
				width=int(self.width*0.60), height=self.height-80)
		self.text_input = ctk.CTkTextbox(self,fg_color=os.getenv("INPUT_BAR_COLOR"),width=int(self.width*0.60)-80, height=35)

		self.contact_frame = ctk.CTkScrollableFrame(self,fg_color='#242424',orientation='vertical',
				width=int(self.width*0.35), height=self.height-35,scrollbar_fg_color='#242424',scrollbar_button_color='#242424',
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

	def add_contact(self):
		if not self.add_entry.get().strip() or self.current_contact is not None and self.current_contact == self.add_entry.get(): return
		contact = ctk.CTkButton(self.contact_frame,text=self.add_entry.get(),fg_color='#242424',hover_color='#555555',anchor='w',
						  height=70)
		contact.bind('<Button-1>',lambda e: self.contact_button_clicked(contact.cget('text')))
		contact.configure(font=self.CONTACT_FONT)
		contact.grid(row=len(self.contact_frame.children), column=0, sticky='we',pady=(20, 10))
		separator_line = ctk.CTkCanvas(self.contact_frame, height=1, bg='#555555', highlightthickness=0)
		separator_line.grid(row=len(self.contact_frame.children), column=0, sticky='we', pady=(20, 10))

	def spawn_message(self, sticky: Literal['e','w'] = 'e', message: Optional[str] = None, attachment: Optional[bytes] = None):
		#'e' para derecha, 'w' para izquierda
		if self.current_contact is None:
			raise ValueError('No contact selected')
		color = os.getenv("TEXT_BUBBLE_COLOR")
		if not message:
			message = self.text_input.get('1.0', 'end').strip()
			self.text_input.delete('1.0', 'end')
			if sticky == 'e':
				if not message.strip() and not attachment:
					return
				try:
					data = sendrequests.send_message(self.token,self.current_contact,message,attachment)
					self.rate_limited = False
				except sendrequests.RateLimited as e:
					color = 'red'
					if not self.rate_limited:
						self.rate_limited = True
						messagebox.showerror(f'Error', str(e))
						self.rate_limited = False
		message_box = ctk.CTkLabel(self.frame,width=200,text=message,text_color=os.getenv("TEXT_COLOR"),fg_color=color if sticky == 'e' else '#3C3C3C',
					corner_radius=20,anchor='ne',padx=0, pady=20,wraplength=500)
		if attachment is not None: message_box.configure(image=ctk.CTkImage(Image.open(BytesIO(attachment)),size=(200,200)),compound='bottom')
		message_box.configure(height=message_box.winfo_reqheight()+28) #For some reason text in label f*cks up the height and it looks bad
		message_box.grid(row=len(self.messages), column=0, sticky=sticky,pady=(20, 0))
		self.frame._parent_canvas.update_idletasks()
		self.frame._parent_canvas.config(scrollregion=self.frame._parent_canvas.bbox("all"))
		self.frame._parent_canvas.yview_moveto(1.0)
		self.messages.append({'recipient':self.current_contact,'widgets':message_box,'grid_info':message_box.grid_info()}) #type: ignore

	def on_key_press(self, event: Event):
		if event.keysym == "h": #quick test
			self.spawn_message('w','Hola')
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
		else:
			for widget in self.frame.winfo_children():
				widget.grid_forget()
			for message in self.messages:
				if message['recipient'] == text:
					message['widgets'].grid(**message['grid_info']) #type: ignore
		for pending_message in self.pending_messages.copy():
			self.pending_messages.remove(pending_message)
			if pending_message['sender'] == text:
				self.spawn_message('w',pending_message['message'])

	def open_attachment(self):
		file = ctk.filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;")])
		print(file)
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