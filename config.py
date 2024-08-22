import customtkinter as ctk
from PIL import Image
from tkinter import colorchooser

def center_window_to_display(screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0) -> str:
	screen_width = screen.winfo_screenwidth()
	screen_height = screen.winfo_screenheight()
	x = int((screen_width/2) - (width/2) * scale_factor)
	y = int((screen_height/2) - (height/2) * scale_factor)
	return f'{width}x{height}+{x}+{y}'

config = ctk.CTk()
config.iconbitmap('assets\\logo.ico')
config.title('Java Connect')
config.resizable(False, False)
config.geometry(center_window_to_display(config, 960, 610))

#functions
def background_color():   
    color = colorchooser.askcolor()[1]
    background_color_label = ctk.CTkLabel(config,text="",fg_color=color,width=20,height=20)
    background_color_label.grid(row=2,column=0,padx=(135,0),pady=(35,0))

def text_color():
    text_color = colorchooser.askcolor()[1]
    text_color_label = ctk.CTkLabel(config,text="",fg_color=text_color,width=20,height=20)
    text_color_label.grid(row=3,column=0,padx=(135,0),pady=(10,0))

def text_bubble_color():
    text_bubble_color = colorchooser.askcolor()[1]
    text_bubble_color_label = ctk.CTkLabel(config,text="",fg_color=text_bubble_color,width=20,height=20)
    text_bubble_color_label.grid(row=4,column=0,padx=(135,0),pady=(10,0))

def input_bar_color():
    input_bar_color = colorchooser.askcolor()[1]
    input_bar_color_label = ctk.CTkLabel(config,text="",fg_color=input_bar_color,width=20,height=20)
    input_bar_color_label.grid(row=5,column=0,padx=(135,0),pady=(10,0))

def request():
    #TODO: send request to server
    pass


#define grid
config.grid_columnconfigure((0,1,2,3),weight=0)
config.grid_rowconfigure((0,1,2,3,5,6,7),weight=0)

#user info
pfp = ctk.CTkImage(Image.open('assets\\j.png'),size=(80,80))
pfp_label = ctk.CTkLabel(config,image=pfp,text='')
pfp_label.grid(row=0,column=0,padx=(135,0),pady=(70,0))

username=ctk.CTkEntry(config,placeholder_text='Test',height=30, width=273,font=ctk.CTkFont('SegoeUi',size=20),fg_color='#242424',border_color='#242424')
username.grid(row=0,column=1,stick='W',padx=(10,0),pady=(70,0))

password = ctk.CTkEntry(config,placeholder_text='****',height=30, width=273,font=ctk.CTkFont('SegoeUi',size=20),fg_color='#242424',border_color='#242424')
password.grid(row=1,column=1,stick='W',padx=(10,0),pady=(35,0))

#theme customization
background_label = ctk.CTkLabel(config,text='Color de fondo',font=ctk.CTkFont('SegoeUi',size=20))
background_label.grid(row=2,column=1,stick='W',padx=(10,0),pady=(35,0))
background_color = ctk.CTkButton(config,text='Cambiar',width=40,height=20,command=background_color,)
background_color.grid(row=2,column=2,stick='W',padx=(10,0),pady=(35,0))

text_color_label = ctk.CTkLabel(config,text='Color de texto',font=ctk.CTkFont('SegoeUi',size=20))
text_color_label.grid(row=3,column=1,stick='W',padx=(10,0),pady=(10,0))
text_color = ctk.CTkButton(config,text='Cambiar',width=40,height=20,command=text_color)
text_color.grid(row=3,column=2,stick='W',padx=(10,0),pady=(10,0))

text_bubble_color_label = ctk.CTkLabel(config,text='Color fondo de texto',font=ctk.CTkFont('SegoeUi',size=20))
text_bubble_color_label.grid(row=4,column=1,stick='W',padx=(10,0),pady=(10,0))
text_bubble_color = ctk.CTkButton(config,text='Cambiar',width=40,height=20,command=text_bubble_color)
text_bubble_color.grid(row=4,column=2,stick='W',padx=(10,0),pady=(10,0))

input_bar_color_label = ctk.CTkLabel(config,text='Color de barra de texto',font=ctk.CTkFont('SegoeUi',size=20))
input_bar_color_label.grid(row=5,column=1,stick='W',padx=(10,0),pady=(10,0))
input_bar_color = ctk.CTkButton(config,text='Cambiar',width=40,height=20,command=input_bar_color)
input_bar_color.grid(row=5,column=2,stick='W',padx=(10,0),pady=(10,0))

#save button
save = ctk.CTkButton(config,text='Guardar',width=273,height=35,command=request)
save.grid(row=6,column=1,pady=(35,0))


config.mainloop()