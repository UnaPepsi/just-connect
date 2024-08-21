import customtkinter as ctk

window = ctk.CTk()

text = ctk.CTkTextbox(window)

scroll = ctk.CTkScrollbar(window)
scroll.pack(side='right', fill='y')

scroll.configure(command=text.yview)
text.configure(yscrollcommand=scroll.set)
text.pack(side='left', fill='both', expand=True)

window.geometry('1200x800')
window.mainloop()