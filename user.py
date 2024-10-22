from tkinter import *
from PIL import ImageTk,Image
import sqlite3
import tkinter.messagebox as message
from gtts import gTTS
import pygame
import os
import random
# connection 
conn=sqlite3.connect("arline.db")
cur=conn.cursor()
# flights
cur.execute(''' CREATE TABLE IF NOT EXISTS flights(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  flight_number VARCHAR NOT NULL,
  origin VARCHAR NOT NULL,
  destination VARCHAR NOT NULL,
  departure_time VARCHAR NOT NULL,
  arrival_time VARCHAR NOT NULL
  
)''')
# passengers
cur.execute(''' CREATE TABLE IF NOT EXISTS passengers(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR NOT NULL,
  gender VARCHAR NOT NULL,
  age VARCHAR NOT NULL,
  passport_number VARCHAR NOT NULL,
  contact VARCHAR NOT NULL
  
)''')
# bookings
cur.execute(''' CREATE TABLE IF NOT EXISTS bookings(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  passenger_id INTEGER NOT NULL,
  flight_id INTEGER NOT NULL,
  seat_number VARCHAR NOT NULL,
  FOREIGN KEY(passenger_id) REFERENCES passengers(id),
  FOREIGN KEY(flight_id) REFERENCES flights(id)
  
  
)''')
# for speech recognition
def text_to_speech(text):
  tts=gTTS(text=text, lang='en')
  audio_file="flight_info.mp3"
  tts.save(audio_file)
  
  pygame.mixer.init()
  pygame.mixer.music.load(audio_file)
  pygame.mixer.music.play()
  while pygame.mixer.music.get_busy():
    continue
  pygame.mixer.quit()
  os.remove(audio_file)
def save_passenger():
  name=ent1.get()
  age=entage.get()
  gender=entgender.get()
  passport_number=entpassport.get()
  contact=entcontact.get()
  
  if name=="" or age=="" or gender=="" or passport_number=="" or contact=="":
    message.showinfo("Alert","Please fill in all the fields")
    return
  conn=sqlite3.connect("arline.db")
  cur=conn.cursor()
  cur.execute('''SELECT COUNT(*) FROM passengers WHERE passport_number=?''', (passport_number,))
  exists=cur.fetchone()[0]
  if exists:
    message.showinfo("Error","A passenger with this passport number already exists!")
  else:
    cur.execute(''' INSERT INTO passengers (name,age,gender,passport_number,contact)
                VALUES(?,?,?,?,?)''',(name,age,gender,passport_number,contact))
  conn.commit()
  message.showinfo("Success","Passenger information successully submitted!")
  flight_info=f"Fligt for {name} with {passport_number} is successful"
    # text to speech method
  text_to_speech(flight_info)
  ent1.delete(0,END)
  entage.delete(0,END)
  entgender.delete(0,END)
  entpassport.delete(0,END)
  entcontact.delete(0,END)
  conn.close()
def generate_seat_number():
  seat_numer=f"{random.randint(1,200):03d}"
  seat_row=random.choice(['A','B','C','D'])
  return seat_numer + seat_row
def book_flight(passenger_id,flight_id):
  # connect your database
  conn=sqlite3.connect('arline.db')
  cur=conn.cursor()
  cur.execute(''' SELECT COUNT(*) FROM bookings
              WHERE passenger_id=?  AND flight_id=? 
              ''',(passenger_id,flight_id))
  already_book=cur.fetchone()[0]
  if already_book:
    message.showinfo("Alert", "This flight is already book for that IDs")
  else:
    seat_number=generate_seat_number()
    cur.execute('''INSERT INTO bookings  (passenger_id,flight_id, seat_number)
                VALUES(?,?,?)
                ''',(passenger_id,flight_id,seat_number))
    conn.commit()
    message.showinfo("Success",f"This is your seat number: {seat_number} for you flight")
    flight_info=f"Flight {flight_id} and {passenger_id} for seat number {seat_number} is successful"
    # text to speech method
    text_to_speech(flight_info)
    entpassengerID.delete(0,END)
    entpassport.delete(0,END)
    entflightid.delete(0,END)
    
    conn.close()
def submit_booking():
  try:
    passenger_id=entpassengerID.get()
    flight_id=entflightid.get()
    book_flight(passenger_id,flight_id)
  except ValueError:
    message.showinfo("Input Error","Please enter a valid numeric ids")
    

user=Tk()
user.config(bg="#000000")
user.geometry('1000x500+200+0')
user.title("User Dashboard")
user.resizable(0,0)
spath="images/2.jpg"
simg=ImageTk.PhotoImage(Image.open(spath))
img=Label(user,image=simg, bg="black" , width=300, height=100 )
img.image=simg
img.place(x=0, y=0)
lbl=Label(user, text="User Area", font=("sanseri",50,"bold"), bg="black", fg="#fff", underline=6)
lbl.place(x=400, y=0)

lbl2=Label(user,text="Passenger's Name:", font=("sanserif",12), bg="black", fg="white")
lbl2.place(x=300, y=100)
ent1=Entry(user, width=50)
ent1.place(x=450,y=100)

lblage=Label(user,text="Age:", font=("sanserif",12), bg="black", fg="white")
lblage.place(x=300, y=130)
entage=Entry(user, width=20)
entage.place(x=450,y=130)

lblgender=Label(user,text="Gender:", font=("sanserif",12), bg="black", fg="white")
lblgender.place(x=300, y=160)
entgender=Entry(user, width=20)
entgender.place(x=450,y=160)

lblpassport=Label(user,text="Passport Number", font=("sanserif",12), bg="black", fg="white")
lblpassport.place(x=300, y=190)
entpassport=Entry(user, width=50)
entpassport.place(x=450,y=190)

lblcontact=Label(user,text="Contact Info:", font=("sanserif",12), bg="black", fg="white")
lblcontact.place(x=300, y=220)
entcontact=Entry(user, width=50)
entcontact.place(x=450,y=220)

lblflightid=Label(user,text="flight Id:", font=("sanserif",12), bg="black", fg="white")
lblflightid.place(x=300, y=250)
entflightid=Entry(user, width=50)
entflightid.place(x=450,y=250)

lblpassengerID=Label(user,text="Passenger Id:", font=("sanserif",12), bg="black", fg="white")
lblpassengerID.place(x=300, y=280)
entpassengerID=Entry(user, width=50)
entpassengerID.place(x=450,y=280)

btnsave=Button(user,text="Save Flight", font=("sanserif",12,"bold"), bg="black", fg="white", width=10, command=save_passenger)
btnsave.place(x=450, y=310)

btnbook=Button(user,text="Book Flight", font=("sanserif",12,"bold"), bg="red", fg="white", width=10, command=submit_booking)

btnbook.place(x=580, y=310)

user.mainloop()