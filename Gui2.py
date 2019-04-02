from tkinter import *
from tkinter.ttk import Combobox
from proxy import proxy

class Gui:
    def __init__(self):
        self.window = Tk()
        self.window.title("filtering proxy")
        self.window.geometry('700x500')
        self.allowed_list = []
        self.all_list = [["www.aut.ac.ir","www.art.ac.ir"],["www.theplantlist.org"],["www.partmusic.ir","www.iranhmusic.ir"]]
        self.all_groups = ["universities","nature","art"]
        self.firstbox = None
        self.selected_group=""



        self.frame = Frame(self.window)
        self.frame.pack()

        self.frame1 = Frame(self.frame)
        self.frame1.pack(side=TOP)

        self.frame2 = Frame(self.frame)
        self.frame2.pack()

        self.frame3 = Frame(self.frame)
        self.frame3.pack()

        self.frame4 = Frame(self.frame)
        self.frame4.pack()

        self.frame5 = Frame(self.frame)
        self.frame5.pack(side=BOTTOM)

        self.make_UI()

    def group_clicked(self,name):
        print(name)
        window = Tk()
        window.title()
        window.geometry('300x500')
        index = self.all_groups.index(name)
        label = Label(window, text="this group sites :")
        label.pack(side=TOP)
        for i in self.all_list[index]:
            label = Label(window, text=i)
            label.pack()

    def run_clicked(self,txt3):
        port= txt3.get()
        reslist = list()
        selection = self.firstbox.curselection()
        for i in selection:
            entrada = self.firstbox.get(i)
            reslist.append(entrada)
        for val in reslist:
            index = self.all_groups.index(val)
            print(index)
            for j in self.all_list[index]:
                self.allowed_list.append(j)
            for i in self.allowed_list:
                print(i)
            print(val)
        p = proxy(self.allowed_list,port)
        p.set_connection()

    def make_UI(self):

        # labell = Label(self.window, text="Hello")
        # labell.grid(column=1, row=0)
        labell = Label(self.frame1, text="write the site that you want to add")
        labell.pack(side=TOP)

        txt = Entry(self.frame1, width=20)
        txt.pack(side=BOTTOM)
        label2 = Label(self.frame2, text="write group label of the site ")
        label2.pack(side=TOP)
        txt2 = Entry(self.frame2, width=20)
        txt2.pack()

        label3 = Label(self.frame3, text="to see site in each groups click on group name:")
        label3.pack(side=TOP)
        for index, i in enumerate(self.all_groups):
            btn = Button(self.frame3, text=i, command= lambda i=i : self.group_clicked(i), width=10, padx=0)
            btn.pack(side=LEFT)
        label4 = Label(self.frame4, text="select groups that you don't want to filter : ")
        label4.pack(side=TOP)
        values = StringVar()
        values.set(self.all_groups)
        self.firstbox = Listbox(self.frame4, listvariable=values, selectmode=MULTIPLE, width=20, height=10)
        self.firstbox.pack()

        def clicked():

            group_name = txt2.get()
            if group_name not in self.all_groups:
                self.all_groups.append(group_name)
                self.all_list.append([txt.get()])
            else:
                index = self.all_groups.index(group_name)
                self.all_list[index].append(txt.get())
            self.frame3.destroy()
            self.frame3 = Frame(self.frame)
            self.frame3.pack()


            label3 = Label(self.frame3, text="to see site in each groups click on group name:")
            label3.pack(side=TOP)
            for index, i in enumerate(self.all_groups):
                print(i)
                btn = Button(self.frame3, text=i, command= lambda i=i : self.group_clicked(i), width=10, padx= 0)
                btn.pack(side=LEFT)

            self.frame4.destroy()
            self.frame4 = Frame(self.frame)
            self.frame4.pack(side=BOTTOM)

            label4 = Label(self.frame4, text="select groups that you do not to filter : ")
            label4.pack(side=TOP)
            values = StringVar()
            values.set(self.all_groups)
            self.firstbox = Listbox(self.frame4, listvariable=values, selectmode=MULTIPLE, width=20, height=10)
            self.firstbox.pack()

        btn3 = Button(self.frame2, text="save", command=clicked)
        btn3.pack(side=BOTTOM)

        label = Label(self.frame5, text="write the port that you want run proxy on it :")
        label.pack(side=TOP)
        txt3 = Entry(self.frame5, width=20)
        txt3.pack()
        # port_num = txt3.get()
        # print(">>>>>>>>>",port_num)
        btn4 = Button(self.frame5, text="run proxy", command=lambda m=txt3 : self.run_clicked(m))
        btn4.pack(side=BOTTOM)






        self.window.mainloop()



g = Gui()
