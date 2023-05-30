#Pack
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import threading as th
import time
import sqlite3 as sql
import textwrap
import os
import logging
import _tkinter
import re
TclError = _tkinter.TclError


#clas, py
import util.generic as utl
import root_main as rt
from const  import style
count = 0

options = webdriver.ChromeOptions()
"""options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")"""
userPortable = None
passwordPortable = None
driver = webdriver.Chrome(executable_path=r"./DriverCrome/chromedriver.exe", chrome_options=options)
#status

module_logger = logging.getLogger('main')

class Log(tk.Frame):

    def __init__(self, parent, controller):
            global count
            super().__init__(parent)
            self.grid(column=0, row=0, sticky=tk.NSEW)
            self.configure(background=style.BACKGROUND)
            self.parent = parent
            self.controller = controller
            self.first_open = False
            self.user = tk.StringVar(self)
            self.password = tk.StringVar(self)
            self.loading = loading()
            self.run()
            self.init_labelframe()

    def run(self):
        self.InstanceDB = db_manager()
        self.search_user()
      
    def move_to_home(self):
        self.controller.show_frame(Home)

    def init_labelframe(self):
        tk.Label(
            self, 
            text="Asitente de Tutor es un programa basado en webscraping,\n que escanea los datos del tutor con el fin de organizar y gestionar \n el manejo de la información de los estudiantes\n",
            width="100", 
            justify='center', 
            font=style.FONT_H1,
            fg=style.FONT_COLOR,
            background=style.BACKGROUND,
            ).pack(side='top',
            pady=15)
        
        self.login_img = utl.leer_imagen(r"assets\tutor.png", (400,400))
        label_img_login = tk.Label(self, 
                         image=self.login_img, 
                         background=style.BACKGROUND)
        label_img_login.place(y=200, x=800)

        
        
        data_login = tk.LabelFrame(self, 
                                   text="BO |Tutor", 
                                   padx=30, 
                                   pady=30, 
                                   font=style.FONT_BUTTON,
                                   bg=style.BACKGROUND,
                                   fg=style.BACKGROUND_BLUE
                                   )
        data_login.pack(side='top',
                        pady=15 )
        
        tk.Label(data_login, 
                 text="Usuario: ", 
                 font=style.FONT_H1, 
                 justify=tk.LEFT,
                 bg=style.BACKGROUND,
                 padx=50,
                 ).grid(column=0, row=0)
        
        tk.Entry(data_login, 
                 textvariable=self.user,
                 highlightthickness=3,
                 highlightcolor=style.BACKGROUND_BLUE,
                 font=style.FONT_P,
                 borderwidth=4,
                 bg=style.BACKGROUND_ENTRY,
                 relief=tk.FLAT,
                 justify=tk.CENTER
                 ).grid(column=0, 
                        row=1, 
                        pady=10)
        
        tk.Label(data_login, 
                 text="Contraseña: ", 
                 font=style.FONT_H1, 
                 justify=tk.LEFT,
                 bg=style.BACKGROUND,
                 padx=50,
                 ).grid(column=0, row=2,)
        
        tk.Entry(data_login, 
                 highlightthickness=3,
                 textvariable=self.password,
                 bg=style.BACKGROUND_ENTRY,
                 highlightcolor=style.BACKGROUND_BLUE,
                 font=style.FONT_P,
                 borderwidth=4,
                 relief=tk.FLAT,
                 justify=tk.CENTER,
                 show="*"
                 ).grid(column=0, 
                        row=3, 
                        pady=10)

        tk.Button(data_login, 
                  text="Ingresar",
                  cursor='hand2', 
                  activeforeground=style.BACKGROUND_BLUE, 
                  bg =style.BACKGROUND_BLUE, 
                  activebackground="white", 
                  fg="white", 
                  relief=tk.FLAT,
                  font=style.FONT_BUTTON, 
                  command= lambda: self.login_scrapping(self.user.get(), self.password.get(), True)
                  ).grid(column=0, 
                         row=4, 
                         columnspan=2,
                         pady=5)   
        
        tk.Label(self,
                  text="Ver el codigo:",  
                    justify='center', 
                    font=style.FONT_P,
                    bg=style.BACKGROUND,
                    
                    ).pack(side=tk.TOP ,
                           pady=5,)
        
        link1 = tk.Label(self,
                         text="www.github.com/juan_garay", 
                         fg="blue", 
                         cursor="hand2",
                         bg=style.BACKGROUND)
        link1.pack(side='top'
                    )
        link1.bind("<Button-1>", 
                   lambda e: webbrowser.open_new("http://www.google.com"))
        
        self.run()

    def login_scrapping(self, UserName,UserPass,NewLogin):

        def process1():
            self.loading.start_after(self)
        
        def process2():
            self.login_scrapping1(UserName,UserPass,NewLogin) 
        thread1 = th.Thread(target=process1)
        thread2 = th.Thread(target=process2)
        thread1.start()
        thread2.start()

        


        
    def login_scrapping1(self, UserName,UserPass,NewLogin): 
            global userPortable, passwordPortable
            userPortable = UserName
            passwordPortable = UserPass
               
            driver.get("https://backoffice.kodland.org/en/groups/")
            mBox = driver.find_element("xpath",'//*[@id="id_username"]')
            mBox.send_keys(UserName)
            mBox = driver.find_element("xpath",'//*[@id="id_password"]')
            mBox.send_keys(UserPass)
            button = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[1]/form/button')
            button.click()
            time.sleep(2)
            self.loading.description_process("Comprobando credenciales...")
            url_join = driver.current_url
            if url_join == 'https://backoffice.kodland.org/en/groups/':
                InstaciaADB = db_manager()
                self.loading.description_process("Extrayendo grupos...")
                InstaciaADB.take_groups()
                time.sleep(1)
                if NewLogin == False:
                    save_credential =  messagebox.askquestion(message='Ingreso Exitoso\n ¿Desea guardar el perfil de sua?')
                    if save_credential == 'yes':
                        InstaciaADB.save_credential()
                elif NewLogin == True:
                    self.move_to_home()
                    messagebox.showinfo(message='Ingreso Exitoso')
                self.loading.stop_after()
            else:
                self.loading.stop_after()
                messagebox.showinfo(message='Contraseña o usuario incorrecto', title='Error')
            
    
    def search_user(self):
            self.InstanceDB.openDB()
            self.InstanceDB.cursor.execute("SELECT * FROM Join_Data")
            consul = self.InstanceDB.cursor.fetchone()
            if consul[1] == 'none':
                pass
            else:
                self.first_open = True
                self.user.set(consul[1])
                self.password.set(consul[2])
            return self.InstanceDB.cloesDB()


class Home(tk.Frame):

    def __init__(self, parent, controller, firts_init=None):
        super().__init__(parent)
        self.configure(background=style.BACKGROUND)
        self.controller = controller
        self.init_labelframe_Home()
        self.instanceDB = db_manager()
        self.instSelenuin = Manager_Selenuin()


    def init_labelframe_Home(self):
        """    -----NavBar------     """
        bar = tk.Frame(self, 
                       width=20,
                       bg=style.BACKGROUND_BLUE,
                       relief=tk.SOLID)
        bar.pack(side='left', 
                 expand=tk.NO, 
                 fill=tk.BOTH)
        
        #Imagen del usuario
        self.img = utl.leer_imagen( r"assets\6073874.png", (70,70))
        user_img = tk.Label(bar, 
                         image=self.img, 
                         background=style.BACKGROUND_BLUE)
        user_img.pack(side="top", 
                   pady= 5,
                   padx= 10

                   )
        #Nombre del Usuario
        tk.Label(bar,
                 text="Sin nombre",
                 font=style.FONT_P,
                 bg=style.BACKGROUND_BLUE,
                 fg=style.BACKGROUND   
                 ).pack(side=tk.TOP, 
                        fill="x",
                        pady=10)

        #Botton 1
        self.group = utl.leer_imagen( r"assets\grupo.png", (24,24))

        self.group_button = tk.Button(bar, 
                text=' Grupos ', 
                image=self.group, 
                font=style.FONT_H1, 
                bg=style.BACKGROUND_BLUE,
                relief=tk.FLAT, 
                overrelief=tk.FLAT,
                fg='white',
                compound=tk.LEFT,
                cursor='hand2',
                state=tk.NORMAL,
                justify="left",
                command=lambda: [self.create_body()] )
        
        self.group_button.pack(side=tk.TOP, fill="x")
        
        #Botton 2
        self.meter = utl.leer_imagen( r"assets\metrica.png", (20,20))

        self.meter_button = tk.Button(bar, 
                text=' Metricas ',
                image=self.meter, 
                font=style.FONT_H1, 
                bg=style.BACKGROUND_BLUE,
                relief=tk.FLAT, 
                fg='white',
                cursor='hand2', 
                justify="left",
                compound=tk.LEFT, 
                command=self.hide_group)
        
        self.meter_button.pack(side=tk.TOP, fill="x")
        
        """    -----BODY------     """
        self.boar = tk.Frame(self,
                        bg=style.BACKGROUND,
                        width=800)
        
       
        self.boar.pack(side="left",
                  expand=True,
                  fill=tk.BOTH )
        
        #HEAD OF BODY
        head_label_container = tk.Label(self.boar,
                                bg=style.BACKGROUND,
                                )
        head_label_container.pack(side=tk.TOP,
                                fill="x",
                                 )      
        #Img
        self.outlogin = utl.leer_imagen( r"assets\eye.png", (20,20))

        tk.Button(head_label_container, 
                text='Salir ',
                image=self.outlogin, 
                font=style.FONT_H1, 
                bg=style.BACKGROUND_ENTRY,
                activebackground=style.BACKGROUND_ENTRY,
                relief=tk.GROOVE,
                overrelief=tk.FLAT, 
                fg=style.BACKGROUND_BLUE,
                activeforeground=style.BACKGROUND_BLUE,
                compound=tk.RIGHT,
                cursor='hand2', 
                justify="left",
                ).pack(side=tk.RIGHT,
                            fill=tk.BOTH,
                            padx=15,
                            pady=15 
                            )
          
    def create_body(self):
        try:
            self.table.pack(padx=20)
            self.show_group()
        except: 
            self.show_group()
            self.table = tk.Frame(self.boar, background=style.BACKGROUND)
            self.table.pack(side=tk.RIGHT, padx=20, pady=20)
            body_table = tk.Frame(self.table, pady=5, padx=5, background=style.BACKGROUND )
            body_table.grid(column=0, row=1)
            self.m_style = {'bg': "#c6c9ef",
                    'bg_head': "#223ac1" ,
                    'bg_background': "#6971dd",
                    'bg_background1': "#efefef",
                    'bg_background2': "#d9d9db",
                    "font_h2": ('Arial', 10,'bold'), 
                    "font_h1": ('Arial', 16,'bold'),
                    "font_p": ('Arial', 10, 'bold'),
                    'padx':10,
                    'pady':10,
                    'anchor': tk.CENTER,
                    'fg_head': 'white',
                    'fg_body': '#000000'
                    }
            
            m_style = self.m_style
            
            #HEAD TABLE
            tk.Label(body_table, 
                        text='ID', 
                        bg=m_style["bg_head"], 
                        font=m_style["font_h2"], 
                        anchor=m_style["anchor"], 
                        fg=m_style["fg_head"], 
                        padx=5
                        ).grid(column=0,row=0,
                               sticky=tk.NSEW,
                               padx=2, 
                               pady=4)

            tk.Label(body_table, 
                        text='Grupo', 
                        bg=m_style["bg_head"], 
                        font=m_style["font_h2"], 
                        anchor=m_style["anchor"], 
                        fg=m_style["fg_head"], 
                        padx=5
                        ).grid(column=1,row=0,
                               sticky=tk.NSEW,
                               padx=2, 
                               pady=4)
            tk.Label(body_table, 
                        text='Estudiantes', 
                        bg=m_style["bg_head"], 
                        font=m_style["font_h2"], 
                        anchor=m_style["anchor"], 
                        fg=m_style["fg_head"], 
                        padx=5
                        ).grid(column=2,row=0,
                               sticky=tk.NSEW,
                               padx=2, 
                               pady=4)
            tk.Label(body_table, 
                        text='Curso', 
                        bg=m_style["bg_head"], 
                        font=m_style["font_h2"], 
                        anchor=m_style["anchor"], 
                        fg=m_style["fg_head"], 
                        padx=5
                        ).grid(column=3,row=0,
                               sticky=tk.NSEW,
                               padx=2, 
                               pady=4)
            tk.Label(body_table, 
                        text='Clase anterior', 
                        bg=m_style["bg_head"], 
                        font=m_style["font_h2"], 
                        anchor=m_style["anchor"], 
                        fg=m_style["fg_head"], 
                        padx=5
                        ).grid(column=4,row=0,
                               sticky=tk.NSEW,
                               padx=2, 
                               pady=4)
            tk.Label(body_table, 
                        text='Día', 
                        bg=m_style["bg_head"], 
                        font=m_style["font_h2"], 
                        anchor=m_style["anchor"], 
                        fg=m_style["fg_head"], 
                        padx=5
                        ).grid(column=5,row=0,
                               sticky=tk.NSEW,
                               padx=2, 
                               pady=4)
            tk.Label(body_table, 
                        text='Próxima', 
                        bg=m_style["bg_head"], 
                        font=m_style["font_h2"], 
                        anchor=m_style["anchor"], 
                        fg=m_style["fg_head"], 
                        padx=5
                        ).grid(column=6,row=0,
                               sticky=tk.NSEW,
                               padx=2, 
                               pady=4)
            
            self.instanceDB.openDB()
            self.instanceDB.cursor.execute("SELECT * FROM db_groups")
            list_group = self.instanceDB.cursor.fetchall()
            count=1
            n= 0
            self.loading = loading()
            for row in list_group:
                def ranking_generator(id_group=row[0], n_student_active=row[2], last_lesson=self.wrap(row[4])):
                        def process1():
                            self.loading.start_after(self)
                        def process2():
                            try:
                                ranking_generator_init(id_group, n_student_active, last_lesson) 
                            except:
                                    self.loading.description_process("Reconectadno BO...")
                                    self.instSelenuin.reconectBO()
                                    ranking_generator_init(id_group, n_student_active, last_lesson) 

                            
                        thread1 = th.Thread(target=process1)
                        thread2 = th.Thread(target=process2)
                        thread1.start()
                        thread2.start()


                def ranking_generator_init(id_group, n_student_active, last_lesson):

                    self.instSelenuin.open_new_windows(f"https://backoffice.kodland.org/en/group_{id_group}/")

                    #Extraemos el numero de estudiantes activos
                    st_total =  n_student_active.split(sep='/')
                    st_total = int(st_total[0])
                    
                    self.loading.description_process("Analizando grupo")
                    #Extraer la sesiónes del grupo
                    ss_total = driver.find_element(by=By.XPATH, 
                                                        value='/html/body/div[4]/div[2]/div/div[2]/div/div[1]/table/tbody/tr[9]/td'
                                                        ).text
                    ss_total = ss_total.split(sep='/')
                    ss_total = int(ss_total[0])

                    #Extraer el curso
                    code_curso = driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div[2]/div/div[1]/table/tbody/tr[11]/td').text
                    code_curso = code_curso[1:4]
                    point_total = {'802':[100,200,300,415,535,705,815,915,1025,1105,1205,1305,1405,1505,1605,
                    1645,1745,1845,1915,2005,2105,2205,2295], '663':[125,245,342,465,520,590,710,830,1130,1580,1980,2380,2410,2510,2510,
                    2510,3030,3500,4070,4670,5290,5890,6510,7160,7740,8190,8840,9520,10620,10650,10850,10950,],
                    '714':[116,228,358,488,631,787,598,1128,1310,1508,1717,1933,2120,2354,2604,2689,2789,2899,
                    3025,3161,3305,3458,3623,3798,4262,4684,5138,5448,5900,6150,6330,6450]}

                    # sacar el puntaje disponible
                    point_available = point_total[code_curso][ss_total-1]

                    #DataFrame de los estudiantes
                    df = pd.DataFrame(columns=['Nombre', 'Puesto', 'Puntaje', 'Estado', 'Balance'])
                    st_total_range = st_total * 2
                    for student in range(1, st_total_range, 2):
                        template_link = '//*[@id="test1"]/table/tbody/tr['+str(student)+']'
                        template_balance =  '//*[@id="test1"]/table/tbody/tr['+str(student+1)+']'
                        table = driver.find_element(by=By.XPATH, value=template_link).text
                        table_balance = driver.find_element(by=By.XPATH, value=template_balance).text
                        balance = table_balance.split(sep=':')
                        balance[1] = balance[1].split()
                        balance = (balance[1])
                        vp = table.split(sep='\n')
                        extra = [vp[0],vp[-1]]
                        two = extra[1].split()
                        one= two[0].split(sep='/')
                        two.pop(0)
                        extra.pop(1)
                        extra = extra + [int(one[0])] + [(one[1])] + two + balance
                        extra[2] = int(extra[2])
                        df.loc[len(df)] = extra
                    df_sort = df.sort_values('Puesto') 
                    df_sort.reset_index(inplace=True, drop=True)

                    #Extraer el valor de compromiso
                    compromiso = round((df_sort['Puntaje'].sum()/(point_available*st_total))*100)
                    #Cerramos la ventana
                    self.instSelenuin.close_new_window()
                    #Tomamos el codigo html de nuestra plantilla base y la convertimos en lista para poder modificarla
                    contenido= list()
                    with open(r"ficheros\template.html", "r", encoding='utf-8') as template:
                        for linea in template:
                            columnas = linea.split(';')
                            contenido.append(';'.join(columnas)+'\n')

                    #Modificamos head de la plantilla base
                    
                    curso = {'802':'¡La magia del código con Scratch!', '714': 'Python', '663': 'Scratch'}
                    color_curso = {'802':'Purple', '714': 'blue', '663': 'Orange'}

                    self.loading.description_process("Creando platilla HTML")
                    ll_index = contenido.index('                    <h1 class="last_lesson"></h1>\n\n')
                    Color_index = contenido.index('        --color_theme: var(--Orange)\n\n')
                    pa_index = contenido.index('                    <h1 class="point_ava"></h1>\n\n')
                    cc_index = contenido.index('                    <h1 class="compromiso"></h1>\n\n')
                    name_course_index =contenido.index('                <h2>Python Programming Language</h2>\n\n')
                    contenido[ll_index] = f'                    <h1 class="last_lesson">{last_lesson}</h1>\n\n'
                    contenido[pa_index] = f'                    <h1 class="point_ava">{str(point_available)}</h1>\n\n'
                    contenido[cc_index] = f'                    <h1 class="compromiso">{str(compromiso)}</h1>\n\n'
                    contenido[Color_index] = f'        --color_theme: var(--{color_curso[code_curso]})\n\n'
                    contenido[name_course_index] = f'                <h2>{curso[code_curso]}</h2>\n\n'

                    #Modificamos el body de la plantilla
                    n_index = contenido.index('        <tr class="datos_ranking">\n\n')
                    principal_contend = contenido[0:n_index]
                    secundary_contend = contenido[n_index+5:-1]
                    middle_contend = []
                    for student in range(st_total):
                        perfect = 'nada'
                        if df_sort.iloc[student,2] >= point_available:
                            perfect = 'perfect'
                        name = df_sort.iloc[student,0]
                        name = name.lstrip("-")
                        name = name.lstrip()
                        middle_contend.append('        <tr class="datos_ranking student'+str(df_sort.iloc[student,1])+'">\n\n')
                        middle_contend.append('            <td>'+str(df_sort.iloc[student,1])+'<span></span></td>\n\n')
                        middle_contend.append('            <td>'+name+'</td>\n\n') 
                        middle_contend.append('            <td><div class="container_puntos"><p>'+str(df_sort.iloc[student,2])+'</p></div><meter min="0" max="100" low="32" high="75" optimum="100" value="'+str((int(df_sort.iloc[student,2])/int(point_available))*100)+'"></meter><div class="contain_perfet"><div class="'+perfect+'"> </div></div> </td>\n\n')
                        middle_contend.append('        </tr>\n\n')
                    table_ranking = principal_contend + middle_contend + secundary_contend

                    #Usamos el nuevo codigo html y lo guardamos en otro archivo provisional
                    with open(r"ficheros\temporal_ranking.html", 'w', encoding='utf-8') as archivo:
                        archivo.writelines(table_ranking)
                    self.loading.stop_after()
                    #Abrimos este codigo html
                    url = os.path.abspath(r"ficheros\temporal_ranking.html")
                    webbrowser.open(url)
                
                def detail_groups(id_group=row[0], 
                                name_group=row[1], 
                                n_student=row[2], 
                                curso=self.wrap(row[3]), 
                                last_class= self.wrap(row[4]),
                                next_class=row[6]):
                    
                    def process1():
                        self.loading.start_after(self)
                    def process2():
                        detail_groups_init(id_group, 
                                name_group, 
                                n_student, 
                                curso, 
                                last_class,
                                next_class)
                    thread1 = th.Thread(target=process1)
                    thread2 = th.Thread(target=process2)
                    thread1.start()
                    thread2.start()

                
                def detail_groups_init(id_group, 
                                name_group, 
                                n_student, 
                                curso, 
                                last_class,
                                next_class):
                    


                    window_group= tk.Toplevel()
                    window_group.title(name_group)
                    window_group.config(width=300, height=200)
                    window_group.withdraw()

                    if f"https://backoffice.kodland.org/en/group_{id_group}/" != driver.current_url:
                        self.instSelenuin.open_new_windows(f"https://backoffice.kodland.org/en/group_{id_group}/")

                    m_style = self.m_style

                    """CONTAINER FOR DETAILS OF THE GROUP"""
                    detail_group = tk.Frame(window_group, bg="#7983ff")
                    detail_group.pack(side=tk.LEFT, expand=tk.Y, fill=tk.BOTH, anchor=tk.CENTER ) 


                    """CONTAINER FOR BASIC DETAILS OF THE GROUP"""
                    info_group = tk.Frame(detail_group,padx=12, pady=12, bg=m_style["bg_background"], )
                    info_group.grid(column=0, row=0, ipady=14, sticky=tk.NSEW )

                    """CONTAINER FOR BASIC DETAILS OF THE GROUP"""

                    metricas_group = tk.Frame(detail_group, padx=12, pady=12, bg=m_style["bg_background"],)
                    metricas_group .grid(column=0, row=1,  ipady=14, sticky=tk.NSEW) 

                    student_group = tk.Frame(window_group, padx=12, pady=12, bg="#c6c7ef",)
                    student_group.pack(side=tk.LEFT, expand=tk.Y, fill=tk.BOTH, anchor=tk.CENTER ) 

                    """CONTEND TO METER OF THE GROUP"""
                    #row0
                    tk.Label(info_group, text=name_group, bg=m_style["bg_head"], font=m_style["font_h1"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5, width=30).grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, ipady=5, padx=2)
                    #row1
                    tk.Label(info_group, text= curso, bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=2)
                    #ro2
                    tk.Label(info_group, text=" Estudiantes ", bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=2, column=0, sticky=tk.NSEW, pady=2, padx=2)
                    tk.Label(info_group, text=n_student, bg=m_style["bg"], font=m_style["font_p"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5, ).grid(row=3, column=0, sticky=tk.NSEW, pady=2, padx=2)
                    #row3
                    tk.Label(info_group, text=" Última clase ", bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=2, column=1, sticky=tk.NSEW, pady=2, padx=2)
                    tk.Label(info_group, text=last_class, bg=m_style["bg"], font=m_style["font_p"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5, border=0.5).grid(row=3, column=1, sticky=tk.NSEW, pady=2, padx=2)
                    #row4
                    tk.Label(info_group, text=" Próxima clase:", bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=4, column=0, sticky=tk.NSEW,pady=2, padx=2)
                    tk.Label(info_group, text=next_class, bg=m_style["bg"], font=m_style["font_p"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=4, column=1, sticky=tk.NSEW, pady=2, padx=2)
                            
                    #row 0 HEAD
                    tk.Label(student_group, text="Id", 
                            bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=0, column=0, sticky=tk.NSEW, padx=2, pady=4)
                    tk.Label(student_group, text="Nombre", 
                            bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=0, column=1, sticky=tk.NSEW, padx=2, pady=4)
                    tk.Label(student_group, text="Asistencia", 
                            bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=0, column=2, sticky=tk.NSEW, padx=2, pady=4)
                    tk.Label(student_group, text="Tareas\nentregadas", 
                            bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=0, column=3, sticky=tk.NSEW, padx=2, pady=4)
                    tk.Label(student_group, text=f"% clase", 
                            bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=0, column=4, sticky=tk.NSEW, padx=2, pady=4)
                    tk.Label(student_group, text=f"% casa",
                            bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=0, column=5, sticky=tk.NSEW, padx=2, pady=4)
                    tk.Label(student_group, text=f"%casa", 
                            bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=0, column=6, sticky=tk.NSEW, padx=2, pady=4)
                    tk.Label(student_group, text="No\nRevisadas", 
                            bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=0, column=7, sticky=tk.NSEW, padx=2, pady=4)
                    tk.Label(student_group, text=f"Rank", 
                            bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=0, column=8, sticky=tk.NSEW, padx=2, pady=4)
                    tk.Label(student_group, text=f"Puntaje\ntotal", 
                            bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=0, column=9, sticky=tk.NSEW, padx=2, pady=4)

                    st_total =  n_student.split(sep='/')
                    st_total = int(st_total[0])
                    student_click = driver.find_element(by=By.XPATH, value=f'//*[@id="test1"]/table/tbody/tr[1]/td[1]/div/div[1]/a')
                    link = student_click.get_attribute('href')
                    df = None
                    activity = {}
                    n_class= driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/div/div[2]/div/div[1]/table/tbody/tr[9]/td').text.split('/')
                    n_class = int(n_class[0])
                    activity = extract_activities(n_class, link)
                    
                    for student in range (1, st_total+1):     
                        df_group = self.instanceDB.meter_students(n_class, student, activity)
                        put_student_detail(student, df_group[0], student_group,  m_style, list_no_attend=df_group[1])
                        progress = f"Estudiantes {student}/{st_total}"
                        self.loading.description_process(progress)
                    self.loading.stop_after()
                    self.instSelenuin.close_new_window()
                    
                    """CONTAINER FOR BASIC DETAILS OF THE GROUP"""

                    metricas_group = tk.Frame(detail_group, padx=12, pady=12, bg=m_style["bg_background"],)
                    metricas_group .grid(column=0, row=1,  ipady=14, sticky=tk.NSEW)

                    """CONTEND TO METER OF THE GROUP"""
                    #row0
                    tk.Label(metricas_group, text=f"Métricas de {name_group} ", bg=m_style['bg_head'], font=m_style["font_h1"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5, width=30).grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, pady=5, padx=2)
                    #row1
                    tk.Label(metricas_group, text="Puntaje del grupo", bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=2)
                    tk.Label(metricas_group, text="o_o Bajo", bg=m_style["bg"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=1, column=2,sticky=tk.NSEW, padx=2)
                    #row2
                    tk.Label(metricas_group, text="Asistencia", bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=2, column=0,sticky=tk.NSEW, pady=2, padx=2)
                    tk.Label(metricas_group, text="Rendimiento en clase", bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=2, column=1,sticky=tk.NSEW, pady=2, padx=2)
                    tk.Label(metricas_group, text="Rendimiento en casa", bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=2, column=2,sticky=tk.NSEW, pady=2, padx=2)
                    #row3
                    tk.Label(metricas_group, text="00%", bg=m_style["bg"], font=m_style["font_p"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=3, column=0,sticky=tk.NSEW, pady=2, padx=2)
                    tk.Label(metricas_group, text="00%", bg=m_style["bg"], font=m_style["font_p"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=3, column=1,sticky=tk.NSEW, pady=2, padx=2)
                    tk.Label(metricas_group, text="00%", bg=m_style["bg"], font=m_style["font_p"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=3, column=2,sticky=tk.NSEW, pady=2, padx=2)
                    #row4
                    tk.Label(metricas_group, text="Observaciones", bg=m_style["bg_head"], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_head"], padx=5).grid(row=4, column=0, columnspan=3,sticky=tk.NSEW, pady=2, padx=2)
                    #row5
                    tk.Label(metricas_group, text="00%", bg=m_style["bg"], font=m_style["font_p"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=5, column=0,columnspan=3, sticky=tk.NSEW, pady=2, padx=2)
                
                    window_group.deiconify()
              
                def open_last_recording(id=row[0]):
                    self.instSelenuin.open_new_windows(f"https://backoffice.kodland.org/en/group_{id}")
                    link = driver.find_element(by=By.LINK_TEXT, value="View").get_attribute("href")
                    webbrowser.open_new(str(link))
                    self.instSelenuin.close_new_window()
                    

        
                
                    
                def extract_activities(n_class, link):
                    activity = {}
                    self.instSelenuin.open_new_windows(link, window=2)
                    #Obtenemos el numero de actividades solo aplicar en el primer estudiantes
                    for i in range(1, n_class + 1):   
                        n_activity = driver.find_elements(by=By.XPATH, value=f'//*[@id="full-progress-table"]/tbody/tr[{i}]/td[2]/ul/li')
                        n_activity = len(n_activity)
                        home = 0
                        for j in range(1,n_activity+1):
                            activity_type = driver.find_element(by=By.XPATH, value=f'//*[@id="full-progress-table"]/tbody/tr[{i}]/td[2]/ul/li[{j}]/p')
                            a = activity_type.get_attribute('innerHTML')
                            if a[-2] == 's':
                                home += 1
                        activity[f'L{i}']=[n_activity-home, home] 
                    self.instSelenuin.close_new_window(back_window=1)
                    return activity

                def open_group(event, id=row[0]):
                    webbrowser.open_new(f"https://backoffice.kodland.org/en/group_{id}/")

                def put_student_detail(n_std,df_group, student_group, m_style, list_no_attend):

                    def callBackActivity(event):
                        insALA = ArgumentLabelActivity()
                        insALA.ArgumentLabel(list_no_attend, student_group)
        
                    def open_student(event, id=df_group[0]):
                        webbrowser.open_new_tab(f"https://backoffice.kodland.org/en/student_{id}/")
                        
                    if df_group[5] < 30:
                        id = tk.Frame(student_group, border=0)
                        id.grid(row=n_std, column=0, sticky=tk.NSEW, pady=2)
                        tk.Label(id, text=" ! ", bg='red', font=("Helvetica 12",10, 'bold')).pack(side=tk.LEFT, fill="y")
                        tk.Label(id, text=str(df_group[0]), 
                            bg=m_style[f'bg_background{(n_std%2)+1}'], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).pack(side=tk.LEFT, fill="y")  
                    else:
                        tk.Label(student_group, text=str(df_group[0]), 
                            bg=m_style[f'bg_background{(n_std%2)+1}'], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=n_std, column=0, sticky=tk.NSEW, ipadx=2, ipady=2, pady=2)  
                    text_name = self.wrap(str(df_group[1]))
                    name = tk.Label(student_group, text=text_name, 
                            bg=m_style[f'bg_background{(n_std%2)+1}'], fg="blue",font=m_style["font_h2"], anchor=m_style["anchor"], cursor='hand2', padx=5)
                    name.grid(row=n_std, column=1, sticky=tk.NSEW, ipadx=2, ipady=2, pady=2)
                    name.bind("<Button-1>", open_student)
                    tk.Label(student_group, text=str(df_group[2]),
                            bg=m_style[f'bg_background{(n_std%2)+1}'], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=n_std, column=2, sticky=tk.NSEW, ipadx=2, ipady=2, pady=2)
                    tk.Label(student_group, text=str(df_group[4]),
                            bg=m_style[f'bg_background{(n_std%2)+1}'], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=n_std, column=3, sticky=tk.NSEW, ipadx=2, ipady=2, pady=2)
                    tk.Label(student_group, text=str(df_group[6]),
                            bg=m_style[f'bg_background{(n_std%2)+1}'], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=n_std, column=4, sticky=tk.NSEW, ipadx=2, ipady=2, pady=2)
                    tk.Label(student_group, text=str(df_group[8]),
                            bg=m_style[f'bg_background{(n_std%2)+1}'], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=n_std, column=5, sticky=tk.NSEW, ipadx=2, ipady=2, pady=2)
                    tk.Label(student_group, text=str(df_group[9]),
                            bg=m_style[f'bg_background{(n_std%2)+1}'], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=n_std, column=6, sticky=tk.NSEW, ipadx=2, ipady=2, pady=2)
                    
                    no_attend_label = tk.Label(student_group, text=str(df_group[10]),
                            bg=m_style[f'bg_background{(n_std%2)+1}'], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_body"], cursor='hand2', padx=5)
                    
                    no_attend_label.grid(row=n_std, column=7, sticky=tk.NSEW, ipadx=2, ipady=2, pady=2)
                    if df_group[10] > 1:
                        no_attend_label.bind("<Button-1>", callBackActivity)
                        no_attend_label.config(fg='blue')
                    tk.Label(student_group, text=str(df_group[11]),
                            bg=m_style[f'bg_background{(n_std%2)+1}'], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=n_std, column=8, sticky=tk.NSEW, ipadx=2, ipady=2, pady=2)
                    tk.Label(student_group, text=str(df_group[12]),
                            bg=m_style[f'bg_background{(n_std%2)+1}'], font=m_style["font_h2"], anchor=m_style["anchor"], fg=m_style["fg_body"], padx=5).grid(row=n_std, column=9, sticky=tk.NSEW, ipadx=2, ipady=2, pady=2)
                    
                    Manager_Selenuin
                n += 1
                if n % 2 == 0:
                    bg = style.BACKGROUND_ENTRY
                else:
                    bg = style.BACKGROUND
                row_span = 1
                row4 = self.wrap(row[4])
                row3 = self.wrap(row[3])
                up = False
                line4 = self.newLine(row4)
                line3 = self.newLine(row3)
                if line4 >= 1 or line3>=1:
                    up = True
                    if line4>=line3: 
                        row_span+= line4 
                    else:
                        row_span+= line3
                tk.Label(body_table, text=row[0], 
                         bg=m_style[f'bg_background{(n%2)+1}'], 
                         font=m_style["font_h2"], 
                         anchor=m_style["anchor"], 
                         fg=m_style["fg_body"], padx=5).grid(column=0, 
                                     row=count, 
                                     pady=1, 
                                     rowspan=row_span, 
                                     sticky=tk.NSEW)

                name_group = tk.Label(body_table, text=row[1], bg=m_style[f'bg_background{(n%2)+1}'], font=m_style["font_h2"], anchor=m_style["anchor"], padx=5, fg='Blue', cursor= "hand2" )
                name_group.grid(column=1, row=count, pady=1, rowspan=row_span, sticky=tk.NSEW)
                name_group.bind("<Button-1>", open_group)
                tk.Label(body_table, text=row[2], 
                         bg=m_style[f'bg_background{(n%2)+1}'], 
                         font=m_style["font_h2"], anchor=m_style["anchor"], 
                         fg=m_style["fg_body"], padx=5
                         ).grid(column=2, 
                                row=count, 
                                pady=1, 
                                rowspan=row_span, 
                                sticky=tk.NSEW)
                
                tk.Label(body_table, text= row3, 
                         bg=m_style[f'bg_background{(n%2)+1}'], 
                         font=m_style["font_h2"], 
                         anchor=m_style["anchor"], 
                         fg=m_style["fg_body"], padx=5
                         ).grid(column=3, 
                                row=count, 
                                pady=1, 
                                rowspan=row_span, 
                                sticky=tk.NSEW)
                
                tk.Label(body_table, text= row4, 
                         bg=m_style[f'bg_background{(n%2)+1}'], 
                         font=m_style["font_h2"], 
                         anchor=m_style["anchor"], 
                         fg=m_style["fg_body"], 
                         padx=5
                         ).grid(column=4, 
                                row=count, 
                                pady=1, 
                                rowspan=row_span, 
                                sticky=tk.NSEW)
                
                tk.Label(body_table, text=row[5], 
                         bg=m_style[f'bg_background{(n%2)+1}'], 
                         font=m_style["font_h2"], 
                         anchor=m_style["anchor"], 
                         fg=m_style["fg_body"], 
                         padx=5
                         ).grid(column=5, 
                                row=count, 
                                pady=1, 
                                rowspan=row_span, 
                                sticky=tk.NSEW)
                
                tk.Label(body_table, text=row[6],
                         bg=m_style[f'bg_background{(n%2)+1}'], 
                         font=m_style["font_h2"], 
                         anchor=m_style["anchor"], 
                         fg=m_style["fg_body"], 
                         padx=5
                         ).grid(column=6, 
                                row=count, 
                                pady=1, 
                                rowspan=row_span, 
                                sticky=tk.NSEW)
                
                label_button = tk.Frame(body_table, width=12, bg= style.BACKGROUND_BLUE)
                label_button.grid(column=7, columnspan=3, row=count, rowspan=row_span)
                button_ranking = ImageButton(label_button,
                                    image_path="assets/ranking.png",
                                    text="",
                                    background= style.BACKGROUND,
                                    command= ranking_generator,
                                    
                                    )
                button_ranking.pack(anchor=tk.CENTER, side=tk.LEFT)

                button1_ttp = CreateToolTip(button_ranking, "Ranking")

                button_show = ImageButton(label_button,
                                    image_path="assets/eye.png",
                                    text="",
                                    background= style.BACKGROUND,
                                    command= detail_groups
                                    )
                button_show.pack(anchor=tk.CENTER, side=tk.LEFT)
                
                button2_ttp = CreateToolTip(button_show, "Extraer Contactos")

                button_last_recording = ImageButton(label_button,
                                    image_path="assets/camara.png",
                                    text="",
                                    background= style.BACKGROUND,
                                    command= open_last_recording
                                    )
                button_last_recording.pack(anchor=tk.CENTER, side=tk.LEFT)
                
                button2_ttp = CreateToolTip(button_last_recording, "Ver Grabación")



                
                
                
                if up == True:
                    count+=row_span
                else:
                    count+= 1 

    def newLine(self, linea):
        resultado=linea.splitlines()
        return(len(resultado)-1)

    def wrap(self, string, lenght=25):
        self.row_text = len(string)//30
        return '\n'.join(textwrap.wrap(string, lenght))
    
    def show_group(self,event=None): # Mostrar los widgets por medio de esta función al hacer clic
        self.group_button.config(bg=style.BACKGROUND_ENTRY,
                                 relief=tk.FLAT, 
                                 fg=style.BACKGROUND_BLUE,
                                 command=None)

    def hide_group(self, event=None): # Ocultar los widgets por medio de esta función al hacer clic
        self.group_button.config(bg=style.BACKGROUND_BLUE, 
                                 relief=tk.FLAT, 
                                 fg=style.BACKGROUND_ENTRY)
        self.table.pack_forget() 

class ArgumentLabelActivity:      
    
    def ArgumentLabel(self, no_activity,student):
        window_no_attend = tk.Toplevel(bg=style.BACKGROUND)
        window_no_attend.title("Actividades no revisadas")
        row_label=0
        columm_label=0
        for lesson in no_activity.keys():
            mainLabel= tk.Frame(window_no_attend, bg=style.BACKGROUND)
            mainLabel.pack(side=tk.TOP, fill="x", anchor="e")
            tk.Label(mainLabel, text=f'{lesson}:', bg=style.BACKGROUND).grid(column=0, row=row_label)
            for activity in no_activity[lesson][0]:
                columm_label+=1
                label = tk.Button(mainLabel, text=activity, fg='blue', bg=style.BACKGROUND, relief=tk.FLAT)
                label.grid(column=columm_label, row=row_label)
                label.bind("<Button-1>", lambda : webbrowser.open_new(no_activity[lesson][1][columm_label-1]))
        row_label+=1
               

class db_manager():

    def openDB(self): 
        self.bsd = sql.connect("ficheros/TutorBase.db")
        self.cursor = self.bsd.cursor()

    def cloesDB(self):
        self.bsd.close()

    def saveDB(self):
        return self.bsd.commit()

    def save_credential(self):
        self.openDB()
        self.cursor.execute(f"UPDATE Join_Data SET User = '{self.user}', Password = '{self.password}' WHERE  ID = '1'" )
        self.saveDB()
        return self.cloesDB 
    
    def take_groups(self):
        curso = {'802':'¡La magia del código con Scratch!', '714': 'Python', '663': 'Scratch'}
        soup = BeautifulSoup(driver.page_source)
        n_tablegroup = len(soup.find_all('a', class_="endless_page_link"))
        if n_tablegroup == 0:
            n_tablegroup = 1
        count=0
        self.openDB()
        self.cursor.execute('DELETE FROM db_groups;')
        for table in range(n_tablegroup):
            n_group = int(len(soup.find_all('a', class_="table-link"))/2)
            for group in range(n_group):
                id = driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/table/tbody/tr['+str(group+1)+']/td[1]').text
                namegroup = driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/table/tbody/tr['+str(group+1)+']/td[2]').text
                sa = driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/table/tbody/tr['+str(group+1)+']/td[3]').text
                c = driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/table/tbody/tr['+str(group+1)+']/td[4]').text
                try :
                    c = curso[c[1:4]]
                except:
                    c = 'undefine'
                ls = driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/table/tbody/tr['+str(group+1)+']/td[7]').text
                ultima_clase = driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/table/tbody/tr['+str(group+1)+']/td[6]').text
                ultima_clase= ultima_clase[:-6]
                ahora = datetime.now()
                last_class = datetime.strptime(ultima_clase, "%d.%m.%Y")
                y_t = int(abs(((last_class+timedelta((int(((ahora - last_class)//7).total_seconds())//86400)*7))-ahora).total_seconds()//86400)) 
                if y_t == 7:
                    y_t = "Mañana"
                elif (8-y_t) == 7:
                    y_t = "Hoy"
                else:
                    y_t = f"En {str(8-y_t)} dias"
                s_t = str(last_class+timedelta((int(((ahora - last_class)//7).total_seconds())//86400)*7))
                s_t= s_t[:-9]
                row = f"{id},'{namegroup}','{sa}','{c}','{ls}','{s_t}','{y_t}'"
                self.cursor.executescript(f"INSERT INTO db_groups VALUES ({(row)})")
            if table < n_tablegroup-1:
                driver.find_element(by=By.XPATH, value='//*[@id="table_to_change"]/ul/li[3]/a').click()
                time.sleep(3)
                soup = BeautifulSoup(driver.page_source)
        self.saveDB()
        return self.cloesDB()

    def meter_students(self, n_class, student, activity):
            InstMS = Manager_Selenuin()
            #Obtenemos la asistencia desde el grupo
            assis_history = []

            line= 1
            m1 = 1
            lesson = 0
            n_attend = 0
            n_absence = 0
            n_miss = 0
            n_error = 0
            for less in range(1,n_class+1):
                if m1 == 5:
                    m1 = 1
                    line=2  
                if lesson == 4:
                    lesson = 0  
                    m1 +=1
                lesson +=1
                attend = len(driver.find_elements(by=By.CSS_SELECTOR, value=f'#test1 > table > tbody > tr:nth-child(1) > td:nth-child(2) > ul:nth-child({line})>div:nth-child({m1})>div:nth-child(2)>div:nth-child({lesson})>div.student_attendance.student_attendance-to_edit.student_attendance-attend'))
                if attend == 1:
                    assis_history.append('attend')
                    n_attend += 1
                miss = len(driver.find_elements(by=By.CSS_SELECTOR, value=f'#test1 > table > tbody > tr:nth-child(1) > td:nth-child(2) > ul:nth-child({line})>div:nth-child({m1})>div:nth-child(2)>div:nth-child({lesson})>div.student_attendance.student_attendance-to_edit.student_attendance-miss'))
                if miss == 1:
                    assis_history.append('miss')
                    n_miss +=1
                    continue
                absence =  len(driver.find_elements(by=By.CSS_SELECTOR, value=f' #test1 > table > tbody > tr:nth-child(1) > td:nth-child(2) > ul:nth-child({line})>div:nth-child({m1})>div:nth-child(2)>div:nth-child({lesson})>div.student_attendance.student_attendance-to_edit.student_attendance-absence'))
                if absence == 1:
                    assis_history.append('absence')
                    n_absence +=1
                    continue
                error_tutor = len(driver.find_elements(by=By.CSS_SELECTOR, value=f'#test1 > table > tbody > tr:nth-child(1) > td:nth-child(2) > ul:nth-child({line})>div:nth-child({m1})>div:nth-child(2)>div:nth-child({lesson})>div.student_attendance.student_attendance-to_edit.student_attendance-no-att'))
                if error_tutor == 1:    
                    n_error +=1         
                    assis_history.append('error_tutor')
                    continue

                miss_percent = (n_miss / n_class)
                atten_percent = (n_attend / n_class)
            
            if student>1:
                student = student*2-1
            #Extraemos el nombre
            student_click = driver.find_element(by=By.XPATH, value=f'//*[@id="test1"]/table/tbody/tr[{student}]/td[1]/div/div[1]/a')
            link = student_click.get_attribute('href')
            student_name = driver.find_element(by=By.XPATH, value=f'//*[@id="test1"]/table/tbody/tr[{student}]/td[1]/div/div[1]/a').text
            id = link.split('_')
            id = id[1]
            id = id[:-1]
            InstMS.open_new_windows(link, window=2)

            #student_click.click()

            #Extraemos el ID desde el link 

            #Nivel de asistencia
            attend_level = None
            if miss_percent > 80:
                attend_level = 'Muy baja'
            elif miss_percent > 60:
                attend_level = 'Baja'
            elif miss_percent > 40:
                attend_level = 'Regular'
            elif miss_percent > 20:
                attend_level = 'Media'
            elif miss_percent > 10:
                attend_level = 'alta'
            elif miss_percent > 0:
                attend_level = 'Muy alta'
            elif miss_percent == 0:
                attend_level = 'Perfecta'
            

            # Obtnenemos el numero de actividades realizadas  
            
            total_activity_class_miss = 0
            total_activity_class_attend = 0
            total_activity_class_no_attend = 0

            total_activity_home_miss = 0
            total_activity_home_attend = 0
            total_activity_home_no_attend = 0
            no_attend_activity_general = {}

            for n_lesson in range(1, n_class+1):
                status_act_l = []
                activity_class_miss = 0
                activity_class_attend = 0
                activity_class_no_attend = 0

                activity_home_miss = 0
                activity_home_attend = 0
                activity_home_no_attend = 0

                no_attend_activity_lesson = []
                no_attend_activity_lesson_href = []
                
                #Clase
                for n_activity in range(1, (activity[f'L{n_lesson}'][0])+1):
                    miss_ac = len(driver.find_elements(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_activity}) > a > div.student_attendance.student_attendance_mini.student_attendance-miss'))
                    if miss_ac == 1:
                        activity_class_miss +=1
                        continue
                    attend_ac = len(driver.find_elements(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_activity}) > a > div.student_attendance.student_attendance_mini.student_attendance-attend'))
                    if attend_ac == 1:
                        activity_class_attend +=1
                        continue
                    absence_ac = len(driver.find_elements(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_activity}) > a > div.student_attendance.student_attendance_mini.student_attendance-absence'))
                    if absence_ac == 1:
                        no_attend_activity_lesson.append(f'CW{n_activity}')
                        href_no_attend_class =  driver.find_element(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_activity}) > a')
                        href_class = href_no_attend_class.get_attribute('href')
                        activity_class_no_attend +=1
                        no_attend_activity_lesson_href.append(href_class)

                        continue
                #Casa
                for n_activity in range(1, (activity[f'L{n_lesson}'][1])+1):
                    n_act =  n_activity + (activity[f'L{n_lesson}'][0])
                    miss_ac = len(driver.find_elements(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_act}) > a > div.student_attendance.student_attendance_mini.student_attendance-miss'))
                    if miss_ac == 1:
                        activity_home_miss +=1
                        continue
                    attend_ac = len(driver.find_elements(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_act}) > a > div.student_attendance.student_attendance_mini.student_attendance-attend'))
                    if attend_ac == 1:
                        activity_home_attend +=1
                        continue
                    absence_ac = len(driver.find_elements(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_act}) > a > div.student_attendance.student_attendance_mini.student_attendance-absence'))
                    if absence_ac == 1:
                        no_attend_activity_lesson.append(f'HW{n_activity}')
                        href_no_attend_home =  driver.find_element(by=By.CSS_SELECTOR, value=f'#full-progress-table > tbody > tr:nth-child({n_lesson}) > td:nth-child(2) > ul > li:nth-child({n_activity}) > a')
                        href_home = href_no_attend_home.get_attribute('href')
                        no_attend_activity_lesson_href.append(href_home)
                        activity_home_no_attend +=1
                        continue
                if len(no_attend_activity_lesson) >= 1:
                    no_attend_activity_general[f'L{n_lesson}'] = [no_attend_activity_lesson,no_attend_activity_lesson_href]

                total_activity_class_miss += activity_class_miss
                total_activity_class_attend += activity_class_attend
                total_activity_class_no_attend += activity_class_no_attend
                total_activity_home_miss += activity_home_miss
                total_activity_home_attend += activity_home_attend
                total_activity_home_no_attend += activity_home_no_attend


            #Tareas realizadas porcentaje
            total_task = total_activity_class_miss + total_activity_class_attend + total_activity_class_no_attend + total_activity_home_miss + total_activity_home_attend + total_activity_home_no_attend
            total_task_attend = round(((total_activity_class_attend + total_activity_class_no_attend+total_activity_home_attend+total_activity_home_no_attend) / total_task)*100)


            #total de tareas en clase realizadas
            total_task_class_attend = total_activity_class_attend + total_activity_class_miss + total_activity_class_no_attend
            percent_task_class_attend = round(((total_activity_class_attend + total_activity_class_no_attend) / total_task_class_attend)*100)

            #Total de tareas en casa realizadas
            total_task_home_attend = total_activity_home_miss + total_activity_home_attend + total_activity_home_no_attend
            percent_task_home_attend = round(((total_activity_home_attend + total_activity_home_no_attend) / total_task_home_attend)*100)

            
            #Total de actividade no revisadas
            total_task_no_attend = total_activity_home_no_attend + total_activity_class_no_attend

            #Rank y Puntaje
            rank_point = driver.find_element(by=By.XPATH, value=f'/html/body/div[3]/div[2]/div/div[10]/div/div[1]/table/tbody/tr/td[3]').text
            
            rank_point = rank_point.split('/')

            #Rank
            rank = rank_point[0]

            #Puntaje
            point= rank_point[1]

            row =[id, 
                student_name, 
                attend_level,
                round(atten_percent+100),
                 f'{total_activity_class_attend + total_activity_class_no_attend+total_activity_home_attend+total_activity_home_no_attend}/{total_task}',
                total_task_attend,
                f'{total_activity_class_attend + total_activity_class_no_attend}/{total_task_class_attend}',
                percent_task_class_attend,
                f'{total_activity_home_attend + total_activity_home_no_attend}/{total_task_home_attend}',
                percent_task_home_attend,
                total_task_no_attend,
                rank,
                 point
                ]
            InstMS.close_new_window(back_window=1)
            return([row ,no_attend_activity_general])

class ImageButton(tk.Button):
        def __init__(self, parent, image_path=None, bg_ = None, command_=None, *args, **kwargs):
            tk.Button.__init__(self, parent, *args, **kwargs, cursor="hand2", relief=tk.FLAT, bg=bg_, padx=2)
            self.logger = logging.getLogger('main.ImageButton')
            ch = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] <%(name)s>: %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

            self._image_path = None
            self._image = None
            self.image_path = image_path

        @property
        def image_path(self):
            return self._image_path

        @image_path.setter
        def image_path(self, path):
            path = os.path.abspath(path)
            try:
                self._image = tk.PhotoImage(file=path)
                self.config(image=self._image)
                self._image_path = path
            except TclError:
                self.logger.warn("No se pudo cargar la imagen desde '{}'".format(path)) 


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


class Manager_Selenuin():    
    
    def open_new_windows(self, link, window=1):
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[window])
        driver.get(link)
        
    def close_new_window(self, back_window=0):
        driver.close()
        driver.switch_to.window(driver.window_handles[back_window])

    def reconectBO(self):
        global userPortable, passwordPortable
        self.close_new_window()        
        driver.get("https://backoffice.kodland.org/es/login/")
        mBox = driver.find_element("xpath",'//*[@id="id_username"]')
        mBox.send_keys(userPortable)
        mBox = driver.find_element("xpath",'//*[@id="id_password"]')
        mBox.send_keys(passwordPortable)
        button = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[1]/form/button')
        button.click()



class loading():
    def __init__(self) -> None:
        self.framesNum = 30 
        archivo = "Bars.gif"
        self.error = utl.leer_imagen(r'assets\error.png', (200,200))
        # Lista de todas las imagenes del gif
        self.frames = [tk.PhotoImage(file=archivo, format='gif -index %i' %(i)) for i in range(self.framesNum)]

    def update(self,ind):
        self.frame = self.frames[ind]
        ind += 1
        if ind == self.framesNum:
            ind = 0
        self.canvas.create_image(0, 0, image=self.frame, anchor=tk.NW)
        self.after_id_gif = self.root.after(30, self.update, ind) # Numero que regula la velocidad del gif

       
    def start_after(self, root):
        self.description =  tk.StringVar()
        self.description.set("Cargando...")
        self.root = root
        self.label_frame = tk.LabelFrame(self.root, cursor="wait", width=500, height=500, bg="")
        self.label_frame.place(relwidth=1.0, relheight=1.0, relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.canvas = tk.Canvas(self.label_frame, width=200, height=200) # Modificar segun el tamaño de la imagen
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        description_label = tk.Label(self.label_frame, textvariable=self.description)
        description_label.place( relx=0.5, rely=0.62,anchor=tk.CENTER)
        self.after_id = self.root.after(0, self.update, 0)
        

    def stop_after(self):
        self.root.after_cancel(self.after_id_gif)
        self.root.after_cancel(self.after_id)
        self.Quit()
        

    def description_process(self, text):
        self.description.set(text)

    def Except(self, text):
        self.root.after_cancel(self.after_id_gif)
        self.root.after_cancel(self.after_id)
        self.canvas.create_image(0, 0, image=self.error, anchor=tk.NW)
        self.description.set(text)
        tk.Button(self.label_frame, text="Cancelar", command=self.Quit).place(relx=0.5, rely=0.68,anchor=tk.CENTER)
        self.label_frame.config(cursor="")
        
        
    def Quit(self):
        self.label_frame.destroy()