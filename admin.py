

# # # CRUD FULL MEANING
# # C=CREATE
# # R=READ
# # U=UPDATE
# # D=DELETE

# # API MEANING
# # A=APPLICATION
# # P=PROGRAMMING
# # I=INTERFACE

from tkinter import *
from PIL import ImageTk, Image
import sqlite3
import tkinter.messagebox as message
from gtts import gTTS
import pygame
import os
import subprocess

# Database connection
conn = sqlite3.connect("arline.db")
cur = conn.cursor()

# Create tables if they do not exist
cur.execute(''' CREATE TABLE IF NOT EXISTS flights(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  flight_number VARCHAR NOT NULL,
  origin VARCHAR NOT NULL,
  destination VARCHAR NOT NULL,
  departure_time VARCHAR NOT NULL,
  arrival_time VARCHAR NOT NULL
)''')

cur.execute(''' CREATE TABLE IF NOT EXISTS passengers(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR NOT NULL,
  gender VARCHAR NOT NULL,
  age VARCHAR NOT NULL,
  passport_number VARCHAR NOT NULL,
  contact VARCHAR NOT NULL
)''')

cur.execute(''' CREATE TABLE IF NOT EXISTS bookings(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  passenger_id INTEGER NOT NULL,
  flight_id INTEGER NOT NULL,
  age VARCHAR NOT NULL,
  seat_number VARCHAR NOT NULL,
  FOREIGN KEY(passenger_id) REFERENCES passengers(id),
  FOREIGN KEY(flight_id) REFERENCES flights(id)
)''')

admin = Tk()
admin.config(bg="#5e546e")
admin.geometry('1000x500+200+0')
admin.title("Admin Dashboard")
admin.resizable(0, 0)

# Load image
# spath = "images/dashboard.jfif"
# simg = ImageTk.PhotoImage(Image.open(spath))
# img = Label(admin, image=simg, bg="#5e546e", width=300, height=100)
# img.image = simg
# img.place(x=0, y=0)
spath = "images/new.jpg"
simg = ImageTk.PhotoImage(Image.open(spath))
img = Label(admin, image=simg, bg="#5e546e", width=500, height=500)
img.image = simg
img.place(x=0, y=0)

def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en')
        audio_file = "flight_info.mp3"
        tts.save(audio_file)
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
    finally:
        pygame.mixer.quit()
        if os.path.exists(audio_file):
            os.remove(audio_file)

def add():
    flight_number = entf.get()
    origin = ento.get()
    departure_time = entd.get()
    destination = entds.get()
    arrival_time = enta.get()
    
    if flight_number and origin and destination and departure_time and arrival_time:
        conn = sqlite3.connect("arline.db")
        cur = conn.cursor()
        cur.execute('''INSERT INTO flights(flight_number, origin, destination, departure_time, arrival_time) VALUES (?, ?, ?, ?, ?)''',
                    (flight_number, origin, destination, departure_time, arrival_time))
        conn.commit()
        conn.close()
        
        message.showinfo("Success", "Flight added successfully")
        flight_info = f"Flight {flight_number} from {origin} to {destination} has been successfully added. Departure at {departure_time} and arrival at {arrival_time}."
        text_to_speech(flight_info)
        entf.delete(0,END)
        ento.delete(0,END)
        entd.delete(0,END)
        entds.delete(0,END)
        enta.delete(0,END)
    else:
        message.showinfo("Alert", "Please fill the form above")
def user():
    subprocess.Popen(["python", "user.py"])



def search():
    flight_number = entf.get()
    
    if flight_number:
        conn = sqlite3.connect('arline.db')
        cur = conn.cursor()
        cur.execute('''SELECT flight_number, origin, destination, departure_time, arrival_time FROM flights WHERE flight_number=?''', (flight_number,))
        result = cur.fetchone()
        conn.close()
        
        if result:
            flight_info = f"Flight {result[0]} from {result[1]} to {result[2]} departs at {result[3]} and arrives at {result[4]}."
            text_to_speech(flight_info)
            # Display flight details in the entry field
            ento.insert(0, result[1])
            entds.insert(0, result[2])
            entd.insert(0, result[3])
            enta.insert(0, result[4])
        else:
            message.showinfo("Not found", "No flight found with that flight number. Please ensure you book a flight.")
    else:
        message.showinfo("Alert", "Please enter a flight number to search.")

def delete_flight():
    flight_number = entf.get()
    
    if flight_number:
        conn = sqlite3.connect("arline.db")
        cur = conn.cursor()
        
        # Execute the delete statement
        cur.execute('''DELETE FROM flights WHERE flight_number=?''', (flight_number,))
        conn.commit()
        
        # Check if any row was deleted
        if cur.rowcount > 0:
            message.showinfo("Success", f"Flight {flight_number} deleted successfully.")
            text_to_speech(f"Flight {flight_number} has been deleted successfully.")
            # Clear entry fields after deletion
            entf.delete(0, END)
            ento.delete(0, END)
            entds.delete(0, END)
            entd.delete(0, END)
            enta.delete(0, END)
        else:
            message.showinfo("Not found", f"No flight found with flight number {flight_number}.")
        
        conn.close()
    else:
        message.showinfo("Alert", "Please enter a flight number to delete.")

    

def update():
    flight_number=entf.get()
    origin=ento.get()
    destination=entds.get()
    departure_time=entd.get()
    arrival_time=enta.get()
    if flight_number and origin and destination and departure_time and arrival_time:
        conn=sqlite3.connect('arline.db')
        cur=conn.cursor()
        cur.execute(''' update flights
                    set origin=?, destination=?, departure_time=?, arrival_time=?
                    where flight_number=?
                    ''',(origin,destination,departure_time,arrival_time,flight_number))
        conn.commit()
        conn.close()
        if cur.rowcount>0:
            message.showinfo('success','flight successfully updated')

        else:
            message.showinfo("Not found", f"No flight found with flight number {flight_number}.")
        
        conn.close()
    else:
        message.showinfo("Alert", "Please enter a flight number to updated.")


# Right frame for the admin panel
right_frame = Frame(admin, width=500, height=1000, bg="royal blue")
lbl = Label(right_frame, text="Admin Panel", font=("sanserif", 50, "bold"), bg="royal blue", fg="#fff", underline=6)
lbl.place(x=0, y=0)
lbluser = Label(admin, text="click the button below to acess the user dashboard", font=("sanserif", 12,), bg="#5e546e", fg="red", underline=6)
lbluser.place(x=50, y=420)
btnuser = Button(admin, text="click me", fg="white", bg="gray", command=user)
btnuser.place(x=230, y=460)

# Flight entry fields
l1 = Label(right_frame, text="Flight Number:", font=("sanserif", 12, "bold"), bg="royal blue", fg="white")
l1.place(x=50, y=100)
entf = Entry(right_frame, width=50)
entf.place(x=180, y=100)

l2 = Label(right_frame, text="Origin:", font=("sanserif", 12, "bold"), bg="royal blue", fg="white")
l2.place(x=50, y=130)
ento = Entry(right_frame, width=50)
ento.place(x=180, y=130)

l3 = Label(right_frame, text="Departure Time:", font=("sanserif", 12, "bold"), bg="royal blue", fg="white")
l3.place(x=50, y=160)
entd = Entry(right_frame, width=50)
entd.place(x=180, y=160)

l4 = Label(right_frame, text="Arrival Time:", font=("sanserif", 12, "bold"), bg="royal blue", fg="white")
l4.place(x=50, y=190)
enta = Entry(right_frame, width=50)
enta.place(x=180, y=190)

l5 = Label(right_frame, text="Destination:", font=("sanserif", 12, "bold"), bg="royal blue", fg="white")
l5.place(x=50, y=220)
entds = Entry(right_frame, width=50)
entds.place(x=180, y=220)

# Buttons
btnadd = Button(right_frame, text="Add Flight", font=("sanserif", 14, "bold"), fg="white", bg="black", command=add)
btnadd.place(x=180, y=250)

btnsearch = Button(right_frame, text="Search Flight", font=("sanserif", 14, "bold"), fg="white", bg="black", command=search)
btnsearch.place(x=300, y=250)

btnupdate = Button(right_frame, text="Update Flight", font=("sanserif", 14, "bold"), fg="white", bg="black", command=update)
btnupdate.place(x=180, y=300)

btndelete = Button(right_frame, text="Delete Flight", font=("sanserif", 14, "bold"), fg="black", bg="red", command=delete_flight)
btndelete.place(x=320, y=300)
btnclose = Button(right_frame, text="close app", font=("sanserif", 14, "bold"), fg="black", bg="red", command=admin.destroy)
btnclose.place(x=370, y=450)

right_frame.pack(side="right")
admin.mainloop()