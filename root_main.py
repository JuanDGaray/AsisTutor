import tkinter as tk
from const import style
from screen import *
from PIL import Image  

#We import main constructor
class root(tk.Tk):

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.title("Asitente de Tutor 1.0 - By. Juan Garay")
        container = tk.Frame(self) #widget padre que va contener a todos los frames
        container.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand= True,
        ) 
        self.resizable(0, 0)
        container.configure(background=style.BACKGROUND)

        ''''AGREGAMOS UN FOOTER PERMANENTE'''
        self.footer = tk.LabelFrame(
            self, 
            height=30, 
            bg=style.BACKGROUND_BLUE,
            borderwidth=0
            )
        self.footer.pack(
            expand=1, 
            fill='both',
            side='bottom'
            )
        self.status = tk.Label(self.footer,
                                text='Activo ✅', 
                                bg=style.BACKGROUND_BLUE, 
                                fg='white', 
                                padx=10 )
        self.status.pack(side="right")

        self.frame = {}
        for f in (Home, Log):
            frame = f(container, self)
            self.frame[f] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.show_frame(Log)
        print(self.frame)
        

    def show_frame(self, container):
        frame = self.frame[container]
        frame.tkraise()






        


