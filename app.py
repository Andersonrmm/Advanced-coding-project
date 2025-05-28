import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from models.person import person
from models.objective import objective
from persistence import save_person, read_person
import datetime

person = read_person()
if not person:
    name = askstring ("Greetings", "Kindly provide your name")
    person = person(person_id=1, name=name)

root = tk.Tk() 
root.titte = ("Objectives Planner")
    

