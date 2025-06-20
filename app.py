import customtkinter as ctk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from models.person import User
from models.objective import Obj
from persistence import save_person, read_person
import datetime

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

user = read_person()
if not user:
    name = askstring ("Greetings", "Kindly provide your name")
    user = User(person_id=1, name=name)

root = ctk.CTk() 
root.geometry = ("1200x1200")
root.titte = ("Objective Planner")

def open_menu(): 
    menu_text.delete("0.0", "end")
    for objective in user.plan: 
        progress = objective.view_progression()
        report = "Finalized" if progress >= 100 else f"{progress:.1f}% finalized"
        menu_text.insert("end", f"{objective.topic}: {objective.hours_accomplished}/{objective.expected_hours}h {report}\n") 

def insert_objective():
    topic = askstring("Topic of your objective", "Insert your objective here:")
    expected_hours = float(askstring("Expected hours", "Insert the expected hours for this objective:"))
    due_date_str = askstring("Due date", "Insert the due date for this goal (YYYY-MM-DD)")
    due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
    objective = Obj(topic, expected_hours, due_date)
    user.put_objective(objective)
    open_menu()
    messagebox.showinfo("Your objective was placed successfully!")

def log_objective(): 
    if not user.plan:
        messagebox.showwarning("Currently, there are no objectives","Add a objective first")
        return
    options = [obj.topic for obj in user.plan]
    option = askstring("Select objective", f"Which objective? ({', '.join(options)})")
    
    selected_objective = [obj for obj in user.plan if obj.topic.lower() == option.lower()]
    if not selected_objective:
        messagebox.showwarning("The selected objective was not found")
        return
    expected_hours = float(askstring("Completed hours", "How many hours have you completed?"))
    selected_objective[0].track_time(expected_hours)
    open_menu()
    messagebox.showinfo("Your completed hours were placed successfully")

def display_status():
    status = ""
    for objective in user.plan: 
        status += f"\n {objective.topic} - Expected hours: {objective.expected_hours}h Completed hours: {objective.hours_accomplished}h\n"
        for date, h in objective.history: 
            status += f"{date} - {h}h\n"
        messagebox.showinfo("Objective record", status or "There is currently no data available" )

def save_exit():
    save_person(user)
    root.quit
        
ctk.CTkButton(root, text="Save and exit", command= save_exit, width= 25).pack(pady= 10)
ctk.CTkButton(root, text="Display status", command= display_status, width= 25).pack(pady= 10)
ctk.CTkButton(root, text="Log objective duration", command= log_objective, width= 25).pack(pady= 10)
ctk.CTkButton(root, text="Insert objective", command= insert_objective, width= 25).pack(pady= 10)

menu_text = ctk.CTkTextbox(root, width= 700, height= 400)
menu_text.pack(pady = 20)
open_menu()

root.mainloop()