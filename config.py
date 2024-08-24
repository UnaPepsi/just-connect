import customtkinter as ctk
import os
import shutil
from dotenv import load_dotenv, dotenv_values, set_key
from customtkinter import filedialog 
from PIL import Image,ImageDraw, ImageOps
from tkinter import colorchooser
from chat import Chat


def center_window_to_display(screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0) -> str:
	screen_width = screen.winfo_screenwidth()
	screen_height = screen.winfo_screenheight()
	x = int((screen_width/2) - (width/2) * scale_factor)
	y = int((screen_height/2) - (height/2) * scale_factor)
	return f'{width}x{height}+{x}+{y}'


load_dotenv("config.env")
config = ctk.CTk()
config.iconbitmap('assets\\logo.ico')
config.title('Java Connect')
config.resizable(False, False)
config.geometry(center_window_to_display(config, 960, 610))

# Variables
selected_values = {
    'background_color': None,
    'text_color': None,
    'text_bubble_color': None,
    'input_bar_color': None,
    'pfp_path': None,
    'pfp_source_path': None,
    'final_Pfp_value': None
}


# Functions

def make_circle(image_path):
    img = Image.open(image_path).convert("RGBA")
    size = (80, 80)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

def choose_color(key, row, column, padx, pady):
    color = colorchooser.askcolor()[1]
    if color:
        selected_values[key] = color
        color_label = ctk.CTkLabel(config, text="", fg_color=color, width=20, height=20)
        color_label.grid(row=row, column=column, padx=padx, pady=pady)

def background_color():
    choose_color('background_color', row=2, column=0, padx=(135, 0), pady=(35, 0))

def text_color():
    choose_color('text_color', row=3, column=0, padx=(135, 0), pady=(10, 0))

def text_bubble_color():
    choose_color('text_bubble_color', row=4, column=0, padx=(135, 0), pady=(10, 0))

def input_bar_color():
    choose_color('input_bar_color', row=5, column=0, padx=(135, 0), pady=(10, 0))

def pfp_button_callback():   
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if filename:
        current_path = os.getcwd()
        destination_path = os.path.join(current_path, 'assets', os.path.basename(filename))
        selected_values['pfp_source_path'] = filename
        selected_values['pfp_path'] = destination_path
        pfp_name_string = selected_values['pfp_path'].split('\\')
        pfp_name_string = pfp_name_string[-1]
        selected_values['final_Pfp_value'] = "assets\\" + "\\" +pfp_name_string
        #print(xd)
        #print(final_Pfp_value)
        #print(selected_values['pfp_source_path'])
        #print(selected_values['pfp_path'])
        #shutil.copy2(filename, destination_path)

def back_button_callback():
    config.destroy()
    Chat(1800,800).mainloop()

def save_button_callback():
    
    if selected_values['background_color']:
        set_key("config.env", "BACKGROUND_COLOR", selected_values['background_color'])
    if selected_values['text_color']:
        set_key("config.env", "TEXT_COLOR", selected_values['text_color'])
    if selected_values['text_bubble_color']:
        set_key("config.env", "TEXT_BUBBLE_COLOR", selected_values['text_bubble_color'])
    if selected_values['input_bar_color']:
        set_key("config.env", "INPUT_BAR_COLOR", selected_values['input_bar_color'])
    if selected_values['pfp_source_path'] and selected_values['pfp_path']:         
        shutil.copy2(selected_values['pfp_source_path'], selected_values['pfp_path'])
    if selected_values['final_Pfp_value']:
        set_key("config.env", "PROFILE_PHOTO", selected_values['final_Pfp_value'])
    #print("Saved values:", selected_values)

#define grid
config.grid_columnconfigure((0,1,2,3),weight=0)
config.grid_rowconfigure((0,1,2,3,5,6,7),weight=0)

#user info
pfp_path = os.getenv('PROFILE_PHOTO')
if pfp_path is None: pfp_path = 'assets\\Guest_Pfp.png'
circular_pfp = make_circle(pfp_path)
pfp = ctk.CTkImage(circular_pfp,size=(80,80))
pfp_button = ctk.CTkButton(config, image=pfp, border_width=0, text='',fg_color='#242424',hover_color='#242424',command=pfp_button_callback)
pfp_button.grid(row=0,column=0,padx=(135,0),pady=(70,0))
#pfp_label = ctk.CTkLabel(config,image=pfp,text='')
#pfp_label.grid(row=0,column=0,padx=(135,0),pady=(70,0))

username=ctk.CTkEntry(config,placeholder_text='Test',height=30, width=273,font=ctk.CTkFont('SegoeUi',size=20),fg_color='#242424',border_color='#242424')
username.grid(row=0,column=1,stick='W',padx=(10,0),pady=(70,0))

password = ctk.CTkEntry(config,placeholder_text='****',height=30, width=273,font=ctk.CTkFont('SegoeUi',size=20),fg_color='#242424',border_color='#242424')
password.grid(row=1,column=1,stick='W',padx=(10,0),pady=(35,0))

#theme customization
background_label = ctk.CTkLabel(config,text='Color de fondo',font=ctk.CTkFont('SegoeUi',size=20))
background_label.grid(row=2,column=1,stick='W',padx=(10,0),pady=(35,0))
background= ctk.CTkButton(config,text='Cambiar',width=40,height=20,command=background_color,fg_color='#eeeff0',hover_color='#3D3D3D',text_color='#242424')
background.grid(row=2,column=2,stick='W',padx=(10,0),pady=(35,0))

text_color_label = ctk.CTkLabel(config,text='Color de texto',font=ctk.CTkFont('SegoeUi',size=20))
text_color_label.grid(row=3,column=1,stick='W',padx=(10,0),pady=(10,0))
text = ctk.CTkButton(config,text='Cambiar',width=40,height=20,command=text_color,fg_color='#eeeff0',hover_color='#3D3D3D',text_color='#242424')
text.grid(row=3,column=2,stick='W',padx=(10,0),pady=(10,0))

text_bubble_color_label = ctk.CTkLabel(config,text='Color fondo de texto',font=ctk.CTkFont('SegoeUi',size=20))
text_bubble_color_label.grid(row=4,column=1,stick='W',padx=(10,0),pady=(10,0))
text_bubble= ctk.CTkButton(config,text='Cambiar',width=40,height=20,command=text_bubble_color,fg_color='#eeeff0',hover_color='#3D3D3D',text_color='#242424')
text_bubble.grid(row=4,column=2,stick='W',padx=(10,0),pady=(10,0))

input_bar_color_label = ctk.CTkLabel(config,text='Color de barra de texto',font=ctk.CTkFont('SegoeUi',size=20))
input_bar_color_label.grid(row=5,column=1,stick='W',padx=(10,0),pady=(10,0))
input_bar = ctk.CTkButton(config,text='Cambiar',width=40,height=20,command=input_bar_color,fg_color='#eeeff0',hover_color='#3D3D3D',text_color='#242424')
input_bar.grid(row=5,column=2,stick='W',padx=(10,0),pady=(10,0))

#save button
save = ctk.CTkButton(config,text='Guardar',width=273,height=35,fg_color="#eeeff0",hover_color='#3D3D3D',text_color='#242424',command=save_button_callback)
save.grid(row=6,column=1,pady=(35,0))

#exit button
back = ctk.CTkButton(config,text='Salir',width=273,height=35,fg_color="#eeeff0",hover_color='#3D3D3D',text_color='#242424',command=back_button_callback)
back.grid(row=7,column=1,pady=(10,0))

config.mainloop()