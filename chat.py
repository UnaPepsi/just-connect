from PIL import Image
from typing import List, Literal, Optional
import customtkinter as ctk
from tkinter import Event, Text

class Chat(ctk.CTk):
	def __init__(self, width: int, height: int):
		super().__init__()
		self.width = width
		self.height = height
		self.resizable(False, False)
		self.geometry(self.center_window_to_display(self, width, height))
		self._enable_widgets()
		self.bind('<Key>',lambda event: self.on_key_press(event))
		self.messages: List[ctk.CTkLabel] = []

	@staticmethod
	def center_window_to_display(screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0) -> str:
		screen_width = screen.winfo_screenwidth()
		screen_height = screen.winfo_screenheight()
		x = int((screen_width/2) - (width/2) * scale_factor)
		y = int((screen_height/2) - (height/2) * scale_factor)
		return f'{width}x{height}+{x}+{y}'

	def _enable_widgets(self):
		self.send_button = ctk.CTkButton(self,text='',command=self.spawn_message,
								   image=ctk.CTkImage(Image.open('assets\\send.png'),size=(30,30)),
								   width=30,height=30)
		self.send_button.configure(fg_color='transparent',hover_color='#555555')
		self.frame = ctk.CTkScrollableFrame(self,fg_color='#242424',orientation='vertical',
				width=int(self.width*0.75), height=self.height-80)
		self.frame.grid_columnconfigure(0, weight=1)
		self.frame.grid_columnconfigure(1, weight=0)
		self.frame.place(anchor='ne',x=self.width-10,y=10)
		self.text_input = ctk.CTkTextbox(self, width=int(self.width*0.75)-35, height=35)
		self.text_input.place(anchor='se',x=self.width-70,y=self.height-10)
		self.send_button.place(anchor='se',x=self.width-10,y=self.height-10)

	def spawn_message(self, sticky: Literal['e','w'] = 'e', message: Optional[str] = None):
		#'e' para derecha, 'w' para izquierda
		if not message:
			message = self.text_input.get('1.0', 'end').strip()
			if not message.strip():
				return
			self.text_input.delete('1.0', 'end')
		message_box = ctk.CTkLabel(self.frame,width=200,text=message,fg_color='#3AAD3C',
					corner_radius=20,anchor='ne',padx=0, pady=20,wraplength=250)
		message_box.grid(row=len(self.messages), column=0, sticky=sticky,pady=(20, 0))
		self.frame._parent_canvas.update_idletasks()
		self.frame._parent_canvas.config(scrollregion=self.frame._parent_canvas.bbox("all"))
		self.frame._parent_canvas.yview_moveto(1.0)
		self.messages.append(message_box)
	
	def on_key_press(self, event: Event):
		if event.keysym == "Return":
			self.spawn_message()
		elif not isinstance(self.text_input.focus_get(),Text):
			self.text_input.focus_set()
			self.text_input.insert('end',event.char)