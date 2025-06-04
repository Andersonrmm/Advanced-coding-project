import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from models.person import person
from models.objective import Objective
from persistence import save_person, read_person
import datetime

person = read_person()
if not person:
    name = askstring ("Greetings", "Kindly provide your name")
    person = person(person_id=1, name=name)

root = tk.Tk() 
root.geometry = ("800x800")
root.titte = ("Objective Planner")

def open_menu(): 
    menu_text.delete("1.0", tk.END)
    for objective in person.object: 
        progress = objective.get_progress()
        report = "Finalized" if progress >= 100 else f"{progress:.1f}% finalized"
        menu_text.insert(tk.END, f"{objective.topic}: {objective.hours_accomplished}/{objective.expected_hours}h {report}\n") 

def insert_objective():
    topic = askstring("Topic of your objective", "Insert your objective here:")
    expected_hours = float(askstring("Expected hours", "Insert the expected hours for this objective"))
    due_date_str = askstring("Due date", "Insert the due date for this goal")
    due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
    objective = Objective(topic, expected_hours, due_date)
    person.insert_objective(objective)
    open_menu()
    messagebox.showinfo("Your objective was placed sucessfully!")

def log_objective():

    


    

