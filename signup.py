from tkinter import *
import tkinter.messagebox as message
import sqlite3
import subprocess

def signup():
  fullname=entry.get()
  position=entry1.get()
  email=entry2.get()
  password=entry3.get()
  
  if fullname=="" or position=="" or email=="" or password=="":
    message.showinfo("Prompt","Empty record is not allowed, please fill the form properly")
    return
  conn=sqlite3.connect('arline.db')
  cur=conn.cursor()
  # cur=conn.cursor()
  cur.execute(''' CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,fullName VARCHAR (50), email VARCHAR (10), position VARCHAR(10), password VARCHAR (15))''')
  
  try:
    cur.execute(''' INSERT INTO users(fullNAme,position,email,password) VALUES(?,?,?,?)''',(fullname,position,email,password))
    conn.commit()
    message.showinfo("PROMPT","Record Successfully Signup")
    # clear_fields()
    victor.destroy()
    sign_in_page()
  except sqlite3.IntegrityError:
    message.showerror("Error","email already exists")
  finally:
    
    conn.close()
def sign_in_page():
  victor=Tk()
  victor.geometry("500x200+500+0")
  victor.title("Sign in")
  victor.config(bg="black")
  lbl=Label(victor, text="Sign In Here",font=("sanserif",20,"bold"), bg="black", fg="#fff")
  lbl.place(x=150, y=10)
  lbl1=Label(victor,text="userName: ", font=("sanserif",12), bg="black", fg="#fff")
  lbl1.place(x=60,y=50)
  ent1=Entry(victor, width=50)
  ent1.place(x=150,y=50)
  
  lbl2=Label(victor,text="Password: ", font=("sanserif",12), bg="black", fg="#fff")
  lbl2.place(x=60,y=80)
  ent2=Entry(victor, width=50, show="*")
  ent2.place(x=150,y=80)
  
  lbl3=Label(victor,text="Position: ", font=("sanserif",12), bg="black", fg="#fff")
  lbl3.place(x=60,y=110)
  ent3=Entry(victor, width=20)
  ent3.place(x=150,y=110)
  
  # victor.destroy()
  
  def login():
      email=ent1.get()
      password=ent2.get()
      position=ent3.get()
      
      if(email=="" or password==""):
        message.showinfo("Prompt","you are yet to fill your login details completely")
      elif(email=="d@gmail.com" or password==""):
        message.showinfo("Prompt","UNAUTHORIZED USER")
        return
      conn=sqlite3.connect('arline.db')
      cur=conn.cursor()
      cur.execute(''' select * from users WHERE email=? AND password=? ''', (email,password))
      result=cur.fetchone()
      if result:
        message.showinfo("Alert"," Login Successful")
        victor.destroy()
        if position.lower()=="admin":
          open_admin_page()
        elif position=="secretary":
          open_user_page()
        else:
          message.showinfo("Alert","UNAUTHORIZE ACCESS")
      conn.close()
  def open_admin_page():
    subprocess.Popen(["python", "admin.py"])
    
  def open_user_page():
    subprocess.Popen(["python", "user.py"])
    
  btn=Button(victor, text="Sign-in", height=2, width=25, bg="red", fg="#fff", command=login)
  btn.place(x=150, y=140)
  victor.mainloop()
  # sign_in_page()
victor=Tk()
victor.geometry("500x400+500+0")
victor.title("Sign up")
victor.config(bg="black")
victor.resizable(0,0)
label=Label(victor, text="Sign Up Here!", font=("sanserif",20,"bold"), fg="#fff", bg="black", underline=5)
label.place(x=150,y=10)
label1=Label(victor, text="Full Name:", font=("sanserif",8), fg="#fff", bg="black", underline=5)
label1.place(x=100, y=50)
entry=Entry(victor, width=50)
entry.place(x=150, y=50)
label2=Label(victor, text="Position:", font=("sanserif",8), fg="#fff", bg="black", underline=5)
label2.place(x=100, y=80)
entry1=Entry(victor, width=50)
entry1.place(x=150, y=80)

# label3=Label(victor, text="Description:", font=("sanserif",8), fg="#fff", bg="#5e546e", underline=5)
# label3.place(x=90,y=110)
# text=Text(victor, width=40, height=10)
# text.place(x=150, y=110)
label4=Label(victor, text="Email:", font=("sanserif",8), fg="#fff", bg="black", underline=5)
label4.place(x=100, y=110)
entry2=Entry(victor, width=50)
entry2.place(x=150, y=110)
label5=Label(victor, text="Password:", font=("sanserif",8), fg="#fff", bg="black", underline=5)
label5.place(x=100,y=140)
entry3=Entry(victor, width=50, show="*")
entry3.place(x=150, y=140)

btn=Button(victor, text="Sign-up", height=2, width=25, bg="red", fg="#fff", command=signup)
btn.place(x=150, y=170)
lbtn=Button(victor, text="Already registered! sign-in", font=("sanserif",12), command=sign_in_page)
lbtn.place(x=150, y=200)

victor.mainloop()