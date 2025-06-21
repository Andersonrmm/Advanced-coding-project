import customtkinter as ctk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from models.person import User
from models.objective import Obj
from persistence import save_person, read_person
import datetime

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

user = read_person()
if not user:
    name = askstring ("Greetings", "Kindly provide your name")
    user = User(person_id=1, name=name)

planner = ctk.CTk() 
planner.geometry = ("1200x1200")
planner.title("Objective Planner")

panel = ctk.CTkFrame(planner, width=300, corner_radius=0)
panel.pack(fill="x")

ctk.CTkLabel(panel, text= "Menu", font= ctk.CTkFont(size= 20, weight="bold")).pack(pady=20)

ctk.CTkButton(panel, text="Clear All objectives", width= 200, command= lambda: clear_goals()).pack(pady= 10)
ctk.CTkButton(panel, text="Save and Exit", width= 200, command= lambda: save_exit()).pack(pady= 10)
ctk.CTkButton(panel, text="Display Status", width= 200, command= lambda: display_status()).pack(pady= 10)
ctk.CTkButton(panel, text="Log Objectives Duration", width= 200, command= lambda: log_objective()).pack(pady= 10)
ctk.CTkButton(panel, text="Insert Objective", width= 200, command= lambda: insert_objective()).pack(pady= 10)

info = ctk.CTkFrame(panel, corner_radius= 10)
info.pack(expand = True, fill = "both", padx = 20, pady = 20)

tittle_label = ctk.CTkLabel(info, text ="Your Objectives", font=ctk.CTkFont(size= 30, weight="bold"))
tittle_label.pack(pady=25)

menu_text = ctk.CTkTextbox(info, width= 700, height= 400)
menu_text.configure(fg_color = "#ffffff", text_color = "#000000")
menu_text.pack(fill = "y", pady = 20)


def open_menu(): 
    menu_text.delete("0.0", "end")
    for objective in user.plan: 
        progress = objective.view_progression()
        report = "Finalized" if progress >= 100 else f"{progress:.1f}%"
        menu_text.insert("end", f"{objective.topic}: {objective.hours_accomplished}/{objective.expected_hours}h {report}\n") 


def insert_objective():
    def send():
        topic = insert_topic.get()
        try: 
            expected_hours = float(insert_hours.get())
            due_date = datetime.datetime.strptime(insert_date.get(), "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Invalid data", "Please insert a valid data")
            return
        
        objective = Obj(topic, expected_hours, due_date)
        user.put_objective(objective)
        open_menu()
        messagebox.showinfo("Your objective was placed successfully!")
        popup.destroy()

    popup = ctk.CTkToplevel(planner)
    popup.title ("New objective")
    popup.geometry("500x400")

    ctk.CTkLabel(popup, text="Topic:").pack(pady=(20,0))
    insert_topic = ctk.CTkEntry(popup, width= 400)
    insert_topic.pack()

    ctk.CTkLabel(popup, text="Expected Hours:").pack(pady=(20,0))
    insert_hours = ctk.CTkEntry(popup, width= 400)
    insert_hours.pack()

    ctk.CTkLabel(popup, text="Due date (YYYY-MM-DD):").pack(pady=(20,0))
    insert_date = ctk.CTkEntry(popup, width= 400)
    insert_date.pack()

    ctk.CTkButton(popup, text= "Add Objective", command= send).pack(pady = 30)


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

def clear_goals():
    user.plan.clear()
    save_person(user)
    open_menu()
    messagebox.showinfo("All topics were cleared successfully")


def save_exit():
    save_person(user)
    planner.quit

menu_text.insert("0.0", "Greetings from your planner")
open_menu()
planner.mainloop() 