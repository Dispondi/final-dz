import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq


# объявляем главный класс
class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.db = db

        self.btns()
        self.treeview()
        self.view_records()
        

    #добавляем кнопки
    def btns(self):
        #рамка для кнопок
        toolbar = tk.Frame(bg='#D7D8E0',bd=2)
        toolbar.pack(side=tk.TOP,fill=tk.X)

        #иконки кнопок
        self.img_add = tk.PhotoImage(file='./img/add.png')
        self.img_del = tk.PhotoImage(file='./img/delete.png')
        self.img_upd = tk.PhotoImage(file='./img/update.png')
        self.img_srch = tk.PhotoImage(file='./img/search.png')
        self.img_refresh = tk.PhotoImage(file='./img/refresh.png')

        #объявляем кнопки
        btn_add = tk.Button(toolbar,image=self.img_add,bg='#d7d8e0',bd=0,command=self.f_btn_add)
        btn_del = tk.Button(toolbar,image=self.img_del,bg='#d7d8e0',bd=0,command=self.f_btn_del)
        btn_upd = tk.Button(toolbar,image=self.img_upd,bg='#d7d8e0',bd=0,command=self.f_btn_upd)
        btn_srch = tk.Button(toolbar,image=self.img_srch,bg='#d7d8e0',bd=0,command=self.f_btn_srch)
        btn_refresh = tk.Button(toolbar,image=self.img_refresh,bg='#d7d8e0',bd=0,command=self.view_records)

        #отображаем кнопки
        btn_add.pack(side='left')
        btn_del.pack(side='left')
        btn_upd.pack(side='left')
        btn_srch.pack(side='left')
        btn_refresh.pack(side='left')
        
    #делаем таблицу
    def treeview(self):
        columns = ("#1", "#2", "#3","#4","#5")
        self.tree = ttk.Treeview(self, show="headings", columns=columns,height=30)
        
        self.tree.column('#1',width=50)
        self.tree.column('#2',width=260)
        self.tree.column('#3',width=233)
        self.tree.column('#4',width=233)
        self.tree.column('#5',width=233)

        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="ФИО")
        self.tree.heading("#3", text="Номер")
        self.tree.heading("#4", text="Почта")
        self.tree.heading("#5", text="Зарплата")
        
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)

        self.tree.pack(side='left')

    #функции кнопок
    def f_btn_add(self):
        Window()
    
    def f_btn_del(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('DELETE FROM db WHERE id=?',(self.tree.set(selection_item,'#1'),))
            self.db.conn.commit()
            self.view_records()
    
    def f_btn_upd(self):
        Update()
    
    def f_btn_srch(self):
        Search()

    
    #функция для кнопки редактирования
    def update_record(self,name,tel,email,salary):
        self.db.c.execute('UPDATE db SET name=?,tel=?,email=?,salary=? WHERE ID=?',
                          (name,tel,email,salary,self.tree.set(self.tree.selection()[0],
                          '#1')))
        self.db.conn.commit()
        self.view_records()
    
    #функция для кнопки поиска
    def search_records(self,name):
        name = ('%' + name + '%')
        self.db.c.execute("""SELECT * FROM db
                          WHERE name LIKE ?""",(name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row)
         for row in self.db.c.fetchall()]

    #отображение записей в таблице
    def view_records(self):
        self.db.c.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row)
         for row in self.db.c.fetchall()]
    
    #запись данных в таблицу
    def records(self,name,tel,email,salary):
        self.db.insert_data(name,tel,email,salary)

#Окно добавления / шаблон окна
class Window(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_child()
        self.root = app
        
   
    def init_child(self):
        # Заголовок окна
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False,False)
        self.grab_set()
        self.focus_set()

        #подписи
        label_name = tk.Label(self,text='ФИО:')
        label_name.place(x=50,y=20)
        label_select = tk.Label(self,text='Телефон')
        label_select.place(x=50,y=50)
        label_sum = tk.Label(self,text='E-mail')
        label_sum.place(x=50,y=80)
        label_salary = tk.Label(self,text='Зарплата')
        label_salary.place(x=50,y=110)

        #добавляем строку ввода для наименования
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200,y=20)


        #добавляем строку ввода для email
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200,y=50)


        #добвляем строку ввода для телефона
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200,y=80)


        #добвляем строку ввода для зарплаты
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200,y=110)

        #кнопка закрытия дочернего окна
        self.btn_cancel = ttk.Button(self,text='Закрыть',command=self.destroy)
        self.btn_cancel.place(x=300,y=170)


        #кнопка добавления
        self.btn_ok = ttk.Button(self,text='Добавить')
        self.btn_ok.place(x=220,y=170)
        
        #срабатывания по лкм
        self.btn_ok.bind('<Button-1>', lambda event:
                         self.root.records(self.entry_name.get(),
                                           self.entry_email.get(),
                                           self.entry_tel.get(),
                                           self.entry_salary.get()))
        
        self.btn_ok.bind('<Button-1>', lambda event: self.root.view_records(), add='+')
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')

#Окно редактирования позиции 
class Update(Window):
    def __init__(self):
        super().__init__()
        self.init_upd()
        self.root = app
        self.db = db
        
        #проверка на выделение записи
        try:
            self.default_data()
        except IndexError:
            messagebox.showerror(title='Ошибка',message='Выберите запись для редактирования!')
            self.destroy()

    #изобразить окошко
    def init_upd(self):
        self.title('Редактировать позицию')
        self.btn_ok.destroy()
        btn_edit = ttk.Button(self,text='Редактировать позицию')
        btn_edit.place(x=155,y=170)
        btn_edit.bind('<Button-1>', lambda event: self.root.update_record(self.entry_name.get(),
                        self.entry_email.get(),
                        self.entry_tel.get(),
                        self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
    
    #заполнение в окошко выделенной записи
    def default_data(self):
        self.db.c.execute("SELECT * FROM db WHERE id=?",
                          self.root.tree.set(self.root.tree.selection()[0],'#1'))
        row = self.db.c.fetchone()
        self.entry_name.insert(0,row[1])
        self.entry_email.insert(0,row[2])
        self.entry_tel.insert(0,row[3])
        self.entry_salary.insert(0,row[4])

#окно поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app
    
    def init_search(self):
        self.title("Поиск")
        self.geometry('300x100')
        self.resizable(False,False)
        label_search = tk.Label(self,text='Поиск')
        label_search.place(x=50,y=20)
        
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105,y=20,width=150)

        btn_cancel = ttk.Button(self,text='Закрыть',command=self.destroy)
        btn_cancel.place(x=185,y=50)

        btn_search = ttk.Button(self,text='Поиск')
        btn_search.place(x=105,y=50)
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event:
                        self.destroy(), add="+")


#база данных
class DB:
    def __init__(self):
        self.conn = sq.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS db (
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       tel TEXT,
                       email TEXT,
                       salary TEXT
        )""")
        self.conn.commit()
    
    def insert_data(self,name,tel,email,salary):
        self.c.execute("INSERT INTO db(name,tel,email,salary) VALUES(?,?,?,?)",(name,tel,email,salary))
        self.conn.commit()

#точка входа
if __name__ == '__main__':
    #объявляем базу данных
    db = DB()
    
    #объявляем приложение
    app = Main()
    app.title('Список сотрудников компании')
    app.geometry('1000x700+460+190')
    app.resizable(False,False)

    #цикл
    app.mainloop()