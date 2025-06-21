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

planner = ctk.CTk() 
planner.geometry = ("1200x1200")
planner.title = ("Objective Planner")

panel = ctk.CTkFrame(planner, width=300, corner_radius=0)
panel.pack(side = "right", fill="y")

ctk.CTkLabel(panel, text= "Menu", font= ctk.CTkFont(size= 20, weight="bold")).pack(pady=20)

ctk.CTkButton(panel, text="Save and Exit", width= 200, command= lambda: save_exit()).pack(pady= 10)
ctk.CTkButton(panel, text="Display Status", width= 200, command= lambda: display_status()).pack(pady= 10)
ctk.CTkButton(panel, text="Log Objective Duration", width= 200, command= lambda: log_objective()).pack(pady= 10)
ctk.CTkButton(panel, text="Insert Objective", width= 200, command= lambda: insert_objective()).pack(pady= 10)

info = ctk.CTkFrame(planner, corner_radius= 10)
info.pack(side= "right", expand = True, fill = "both", padx = 20, pady = 20)

tittle_label = ctk.CTkLabel(planner, text ="Your Objectives", font=ctk.CTkFont(size= 30, weight="bold"))
tittle_label.pack(pady=25)

menu_text = ctk.CTkTextbox(planner, width= 700, height= 400)
menu_text.configure(fg_color = "#ffffff", text_color = "#000000")
menu_text.pack(pady = 20)

def open_menu(): 
    menu_text.delete("0.0", "end")
    for objective in user.plan: 
        progress = objective.view_progression()
        report = "Finalized" if progress >= 100 else f"{progress:.1f}%"
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
    if not option:
        messagebox.showwarning("No topic was entered")
        return

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
        for date, hrs in objective.history: 
            status += f"{date} - {hrs}h\n"
        messagebox.showinfo("Objective record", status or "There is currently no data available" )

def save_exit():
    save_person(user)
    planner.quit

menu_text.insert("0.0", "Greetings from your planner")
open_menu()
planner.mainloop()