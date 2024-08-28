import customtkinter as ctk
import os
import shutil
from dotenv import load_dotenv, set_key
from customtkinter import filedialog 
from PIL import Image,ImageDraw, ImageOps
from tkinter import colorchooser, messagebox
from typing import TYPE_CHECKING
import sendrequests
from io import BytesIO

if TYPE_CHECKING:
	from chat import Chat

#variables

load_dotenv("config.env")
selected_values = {
	'background_color': '',
	'text_color': '',
	'text_bubble_color': '',
	'input_bar_color': '',
	'pfp_path': '',
	'pfp_source_path': '',
	'final_Pfp_value': ''
}


class Settings(ctk.CTkToplevel):
	def __init__(self,width: int, height: int, chat_window: 'Chat',user_name: str):
		super().__init__()
		# self.pfp = None
		self._user_name = user_name
		self.chat_window = chat_window
		self.pfp_path = os.getenv('PROFILE_PHOTO')
		self.title('Java Connect')
		self.geometry(self.center_window_to_display(self,width,height))
		self.resizable(False, False)
		self.iconbitmap('assets\\logo.ico')
		self._enable_widgets()
	
	@staticmethod
	def center_window_to_display(screen: ctk.CTkToplevel, width: int, height: int, scale_factor: float = 1.0) -> str:
	# Functions
		screen_width = screen.winfo_screenwidth()
		screen_height = screen.winfo_screenheight()
		x = int((screen_width/2) - (width/2) * scale_factor)
		y = int((screen_height/2) - (height/2) * scale_factor)
		return f'{width}x{height}+{x}+{y}'
	
	def make_circle(self,image_path):
		img = Image.open(image_path).convert("RGBA")
		size = (80, 80)
		mask = Image.new('L', size, 0)
		draw = ImageDraw.Draw(mask)
		draw.ellipse((0, 0) + size, fill=255)
		output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
		output.putalpha(mask)
		return output

	def choose_color(self,key, row, column, padx, pady):
		color = colorchooser.askcolor()[1]
		if color:
			selected_values[key] = color #type: ignore
			color_label = ctk.CTkLabel(self, text="", fg_color=color, width=20, height=20)
			color_label.grid(row=row, column=column, padx=padx, pady=pady)

	def background_color(self):
		self.choose_color('background_color', row=2, column=0, padx=(135, 0), pady=(35, 0))

	def text_color(self):
		self.choose_color('text_color', row=3, column=0, padx=(135, 0), pady=(10, 0))

	def text_bubble_color(self):
		self.choose_color('text_bubble_color', row=4, column=0, padx=(135, 0), pady=(10, 0))

	def input_bar_color(self):
		self.choose_color('input_bar_color', row=5, column=0, padx=(135, 0), pady=(10, 0))

	def pfp_button_callback(self):   
		filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])#we ask for the file
		if filename:
			current_path = os.getcwd()
			destination_path = os.path.join(current_path, 'assets', os.path.basename(filename))#we create a destination path towards the assets folder
			selected_values['pfp_source_path'] = filename#we save the path of the file
			selected_values['pfp_path'] = destination_path#we save the destination path
			pfp_name_string = selected_values['pfp_path'].split('\\')
			pfp_name_string = pfp_name_string[-1]#we save the name of the file
			selected_values['final_Pfp_value'] = fr"assets\{pfp_name_string}"#we save the final path of the file inside assets

	def back_button_callback(self):
		self.destroy()
		self.chat_window.custom_settings = None
		self.chat_window.deiconify()

	def save_button_callback(self):
		
		if selected_values['background_color']:
			set_key("config.env", "BACKGROUND_COLOR", selected_values['background_color'])
			self.chat_window.bg_color = selected_values['background_color']
		if selected_values['text_color']:
			set_key("config.env", "TEXT_COLOR", selected_values['text_color'])
		if selected_values['text_bubble_color']:
			set_key("config.env", "TEXT_BUBBLE_COLOR", selected_values['text_bubble_color'])
			self.chat_window._bubble_text_color = selected_values['text_bubble_color']
		if selected_values['input_bar_color']:
			set_key("config.env", "INPUT_BAR_COLOR", selected_values['input_bar_color'])
			self.chat_window.text_input_color = selected_values['input_bar_color']
		if selected_values['pfp_source_path'] and selected_values['pfp_path']:         
			shutil.copy2(selected_values['pfp_source_path'], selected_values['pfp_path'])
		if selected_values['final_Pfp_value']:
			set_key("config.env", "PROFILE_PHOTO", selected_values['final_Pfp_value'])
		self.update_pfp()

		user = self.username.get()
		password = self.password.get()
		buffer = BytesIO()
		self.circular_pfp.save(buffer, format='PNG')
		buffer.seek(0)
		try:
			data = sendrequests.edit_user(self.chat_window.token,user,password,buffer.getvalue())
			self.chat_window.token = data['info']['new_token']
		except sendrequests.BaseException as e:
			messagebox.showerror('Error', str(e))
		else:
			messagebox.showinfo('Éxito','Información actualizada :D')

	def update_pfp(self):
		self.pfp_path = selected_values['final_Pfp_value']
		if not self.pfp_path:
			self.pfp_path = 'assets\\default_pfp.png'
		self.circular_pfp = self.make_circle(self.pfp_path)
		self.pfp = ctk.CTkImage(self.circular_pfp,size=(80,80))
		self.pfp_button.configure(True,image=self.pfp)
		self.pfp_button.update()

	def _enable_widgets(self):
		#define grid
		self.grid_columnconfigure((0,1,2,3),weight=0)
		self.grid_rowconfigure((0,1,2,3,5,6,7),weight=0)

		#user info
		self.pfp_button = ctk.CTkButton(self, border_width=0, text='',fg_color='#242424',hover_color='#242424',command=self.pfp_button_callback)
		self.update_pfp()
		self.pfp_button.grid(row=0,column=0,padx=(135,0),pady=(70,0))


		self.username=ctk.CTkEntry(self,placeholder_text=self._user_name,height=30, width=273,font=ctk.CTkFont('SegoeUi',size=20),fg_color='#242424',border_color='#242424')
		self.username.grid(row=0,column=1,stick='W',padx=(10,0),pady=(70,0))

		self.password = ctk.CTkEntry(self,placeholder_text='****',height=30, width=273,font=ctk.CTkFont('SegoeUi',size=20),fg_color='#242424',border_color='#242424')
		self.password.grid(row=1,column=1,stick='W',padx=(10,0),pady=(35,0))

		#theme customization
		self.background_label = ctk.CTkLabel(self,text='Color de fondo',font=ctk.CTkFont('SegoeUi',size=20))
		self.background_label.grid(row=2,column=1,stick='W',padx=(10,0),pady=(35,0))
		self.background= ctk.CTkButton(self,text='Cambiar',width=40,height=20,command=self.background_color,fg_color='#eeeff0',hover_color='#3D3D3D',text_color='#242424')
		self.background.grid(row=2,column=2,stick='W',padx=(10,0),pady=(35,0))

		self.text_color_label = ctk.CTkLabel(self,text='Color de texto',font=ctk.CTkFont('SegoeUi',size=20))
		self.text_color_label.grid(row=3,column=1,stick='W',padx=(10,0),pady=(10,0))
		self.text = ctk.CTkButton(self,text='Cambiar',width=40,height=20,command=self.text_color,fg_color='#eeeff0',hover_color='#3D3D3D',text_color='#242424')
		self.text.grid(row=3,column=2,stick='W',padx=(10,0),pady=(10,0))

		self.text_bubble_color_label = ctk.CTkLabel(self,text='Color fondo de texto',font=ctk.CTkFont('SegoeUi',size=20))
		self.text_bubble_color_label.grid(row=4,column=1,stick='W',padx=(10,0),pady=(10,0))
		self.text_bubble= ctk.CTkButton(self,text='Cambiar',width=40,height=20,command=self.text_bubble_color,fg_color='#eeeff0',hover_color='#3D3D3D',text_color='#242424')
		self.text_bubble.grid(row=4,column=2,stick='W',padx=(10,0),pady=(10,0))

		self.input_bar_color_label = ctk.CTkLabel(self,text='Color de barra de texto',font=ctk.CTkFont('SegoeUi',size=20))
		self.input_bar_color_label.grid(row=5,column=1,stick='W',padx=(10,0),pady=(10,0))
		self.input_bar = ctk.CTkButton(self,text='Cambiar',width=40,height=20,command=self.input_bar_color,fg_color='#eeeff0',hover_color='#3D3D3D',text_color='#242424')
		self.input_bar.grid(row=5,column=2,stick='W',padx=(10,0),pady=(10,0))

		#save button
		self.save = ctk.CTkButton(self,text='Guardar',width=273,height=35,fg_color="#eeeff0",hover_color='#3D3D3D',text_color='#242424',command=self.save_button_callback)
		self.save.grid(row=6,column=1,pady=(35,0))

		#exit button
		self.back = ctk.CTkButton(self,text='Salir',width=273,height=35,fg_color="#eeeff0",hover_color='#3D3D3D',text_color='#242424',command=self.back_button_callback)
		self.back.grid(row=7,column=1,pady=(10,0))
		