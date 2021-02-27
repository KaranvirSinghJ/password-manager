#!/usr/bin/env python
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.messagebox
import tkinter.font as tkFont
from functools import partial
from tkinter import StringVar, OptionMenu


def query_del(id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""DELETE FROM passwords WHERE id=?""", (id,))
    conn.commit()
    conn.close()


def query(site, user, password, sec, a, be):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""SELECT name FROM sqlite_master WHERE name='passwords'""")
    result = c.fetchall()
    if len(result) == 0:
        c.execute("""CREATE TABLE passwords
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            Website TEXT,
            Username TEXT,
            Password TEXT,
            Security_question TEXT,
            Answer TEXT,
            Backup_Email TEXT)""")
    else:
        pass
    if len(site.get()) == 0 or len(user.get()) == 0 or len(password.get()) == 0:
        tkinter.messagebox.showwarning(title="Missing Required Field", message="Check Username, Password and Website. Make sure they are filled.")
    else:
        if len(sec.get()) == 0 and len(be.get()) == 0:
            c.execute("""INSERT INTO passwords (website, username, password) VALUES (?,?,?)""", (site.get(), user.get(), password.get()))
        elif len(sec.get()) == 0 and len(be.get()) != 0:
            c.execute("""INSERT INTO passwords (website, username, password, Security_Question, Answer, Backup_Email) VALUES (?,?,?,?,?,?)""", (site.get(), user.get(), password.get(), None, None, be.get()))
        elif len(sec.get()) != 0 and len(be.get()) == 0:
            c.execute("""INSERT INTO passwords (website, username, password, Security_Question, Answer, Backup_Email) VALUES (?,?,?,?,?,?)""", (site.get(), user.get(), password.get(), sec.get(), a.get(), None))
        else:
            c.execute("""INSERT INTO passwords (website, username, password, Security_Question, Answer, Backup_Email) VALUES (?,?,?,?,?,?)""", (site.get(), user.get(), password.get(), sec.get(), a.get(), be.get()))
    conn.commit()
    conn.close()
    site.delete(first=0, last=100)
    username.delete(first=0, last=100)
    password.delete(first=0, last=100)
    sq.delete(first=0, last=100)
    answer.delete(first=0, last=100)
    backemail.delete(first=0, last=100)


def View():
    for i in listBox.get_children():
        listBox.delete(i)
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""SELECT name FROM sqlite_master WHERE name='passwords'""")
    result = cur.fetchall()
    if len(result) == 0:
        tkinter.messagebox.showwarning(title="No Information", message="There is no information to display")
    else:
        cur.execute("""SELECT * FROM passwords""")
        rows = cur.fetchall()
        for row in rows:
            listBox.insert("", tk.END, values=row)
    conn.commit()
    conn.close()



def selector(wite):
    for i in listBox.get_children():
        listBox.delete(i)
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""SELECT * FROM passwords WHERE website = ?""", (wite.split("'")[1],))
    result = cur.fetchall()
    for row in result:
        listBox.insert("", tk.END, values=row)
    conn.commit()
    conn.close()


def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()

def do_copy():
    master.clipboard_clear()
    co=""
    for t in [listBox.item(x,"values") for x in listBox.selection()][0][1:]:
        if t == "None":
            pass
        else:
            co += t + " "
    master.clipboard_append(co)

def fetchsites():
    connection = sqlite3.connect("data.db")
    curs = connection.cursor()
    cd = ""
    try:
        curs.execute("""SELECT DISTINCT website FROM passwords""")
    except sqlite3.OperationalError:
        curs.execute("""SELECT name FROM sqlite_master WHERE name='passwords'""")
        result = curs.fetchall()
        if len(result) == 0:
            cd += "None"
    if cd == "None":
        weblist = "None"
    else:
        weblist = curs.fetchall()
    connection.commit()
    connection.close()
    return weblist


master = tk.Tk()
master.title('Password Manager')
x = master.winfo_screenwidth()
y = master.winfo_screenheight()
master.geometry("%dx%d+0+0" % (x, y))
viewheight = y-780

fontStyle = tkFont.Font(family="Lucida Grande", size=20)
fontStyle2 = tkFont.Font(family="Lucida Grande", size=15)
tk.Label(master, text="Add Password", font=fontStyle).grid(row=1, column=1)

tk.Label(master, text="Website").grid(row=3, column=0)
tk.Label(master, text="Username").grid(row=4, column=0)
tk.Label(master, text="Password").grid(row=5, column=0)
tk.Label(master, text="Security Question").grid(row=6, column=0)
tk.Label(master, text="Answer").grid(row=7, column=0)
tk.Label(master, text="Back Up Email").grid(row=8, column=0)


site = tk.Entry(master)
username = tk.Entry(master)
password = tk.Entry(master)
sq = tk.Entry(master)
answer = tk.Entry(master)
backemail = tk.Entry(master)

site.grid(row=3, column=1, pady = 2)
username.grid(row=4, column=1, pady = 2)
password.grid(row=5, column=1, pady = 2)
sq.grid(row=6, column=1, pady = 2)
answer.grid(row=7, column=1, pady = 2)
backemail.grid(row=8, column=1, pady = 2)

tk.Button(master, text='Enter', width=15, height=2, font=fontStyle2, command=lambda: query(site, username, password, sq, answer, backemail)).grid(row=9, column=1, sticky=tk.W, pady=4)

w = fetchsites()
tkvar = StringVar(master)
tkvar.set('None')
tk.OptionMenu(master, tkvar, *w, command=lambda x=None: selector(tkvar.get())).grid(row = 9, column =3)
tk.Label(master, text="Choose Website:").grid(row=9, column=2)

# create Treeview columns
cols = ('Id', 'Site', 'Username', 'Password', 'Security Question', 'Answer', 'Backup Email')
listBox = ttk.Treeview(master, columns=cols, show='headings', height=viewheight)
# set column headings
for col in cols:
    listBox.heading(col, text=col.replace("_", " "))
    if col == "Id":
        listBox.column(col, width=40, stretch=False)
    elif col == "Username":
        listBox.column(col, width=210, stretch=False)
    elif col == "Security Question":
        listBox.column(col, width=200, stretch=False)
    elif col == "Backup Email":
        listBox.column(col, width=200, stretch=False)
    elif col == "Password":
        listBox.column(col, width=210, stretch=False)
    else:
        listBox.column(col, width=200, stretch=False)

listBox.grid(row=14, column=0, columnspan=8)

m = Menu(master, tearoff = 0)
m.add_command(label ="Copy",command=lambda: do_copy())
m.add_command(label ="Delete",command=lambda: query_del([listBox.item(x,"values") for x in listBox.selection()][0][0]))


listBox.bind("<Button-2>", do_popup)

showScores = tk.Button(master, text="Show All Passwords", width=15, height=2, font=fontStyle2, command=lambda:View()).grid(row=9, column=6)

tk.mainloop()
