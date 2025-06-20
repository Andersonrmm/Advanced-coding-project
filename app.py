import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from models.person import person
from models.objective import Obj
from persistence import save_person, read_person
import datetime

user = read_person()
if not user:
    name = askstring ("Greetings", "Kindly provide your name")
    user = person(person_id=1, name=name)

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
    objective = Obj(topic, expected_hours, due_date)
    person.insert_objective(objective)
    open_menu()
    messagebox.showinfo("Your objective was placed successfully!")

def log_objective(): 
    if not person.objective:
        messagebox.showwarning("Currently, there are no objectives","Add a objective first")
        return
    options = [objective.topic for objective in person.objective]
    option = askstring("Select objective", f"Which objective? ({', '.join(options)})")
    selected_objective = [obj for obj in person.objective if obj.little.lower() == option.lower()]
    if not selected_objective:
        messagebox.showwarning("The selected objective was not found")

    expected_hours = float(askstring("Completed hours", "How many hours have you completed?"))
    selected_objective[0].log_objective(expected_hours)
    open_menu()
    messagebox.showinfo("Your completed hours were placed successfully")

def display_status():
    status = ""
    for objective in person.objective: 
        status += f"\n {objective.topic} - Expected hours: {objective.expected_hours}h Completed hours: {objective.completed_hours}h\n"
        for date, h in objective.record: 
            status += f"{date} - {h}h\n"
        messagebox.showinfo("Objective record", status or "There is currently no data available" )

def save_exit():
    save_person(person)
    root.quit
        
tk.Button(root, text="Save and exit", command= save_exit, width= 25).pack(pady= 10)
tk.Button(root, text="Display status", command= display_status, width= 25).pack(pady= 10)
tk.Button(root, text="Log objective duration", command= log_objective, width= 25).pack(pady= 10)
tk.Button(root, text="Insert objective", command= insert_objective, width= 25).pack(pady= 10)

menu_text = tk.Text(root, width= 50, height= 15)
menu_text.pack(pady = 15)
open_menu()

root.mainloop()


    



    


    

