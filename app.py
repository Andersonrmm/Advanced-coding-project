import customtkinter as ctk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from models.person import User # To import user model
from models.objective import Obj #To import objective model 
from persistence import save_person, read_person # To import persistence model
import datetime

# APP visual appeal
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("dark-blue") 

# To create user 
user = read_person()
if not user:
    name = askstring ("Greetings", "Kindly provide your name")
    user = User(person_id=1, name=name)

# Planner/app interface 
planner = ctk.CTk() 
planner.geometry = ("1200x1200")
planner.title("Objective Planner")

# Panel for buttons
panel = ctk.CTkFrame(planner, width=300, corner_radius=0)
panel.pack(fill="x")

# Tittle for the buttons
ctk.CTkLabel(panel, text= "Menu", font= ctk.CTkFont(size= 20, weight="bold")).pack(pady=20)

# To save  
def save_exit(): 
    save_person(user) 

# App buttons 
ctk.CTkButton(panel, text="Clear All Objectives", font=ctk.CTkFont(weight="bold"), width= 200, command= lambda: clear_goals()).pack(pady= 10)
ctk.CTkButton(panel, text="Save", font=ctk.CTkFont(weight="bold"), width= 200, command= lambda: save_exit()).pack(pady= 10)
ctk.CTkButton(panel, text="Display Status", font=ctk.CTkFont(weight="bold"),  width= 200, command= lambda: display_status()).pack(pady= 10)
ctk.CTkButton(panel, text="Log Objectives Duration", font=ctk.CTkFont(weight="bold"), width= 200, command= lambda: log_objective()).pack(pady= 10)
ctk.CTkButton(panel, text="Insert Objective", font=ctk.CTkFont(weight="bold"), width= 200, command= lambda: insert_objective()).pack(pady= 10)

# Panel for the white dashboard 
info = ctk.CTkFrame(panel, corner_radius= 10)
info.pack(expand = True, fill = "both", padx = 20, pady = 20)

# Dashboard tittle 
tittle_label = ctk.CTkLabel(info, text ="Your Objectives", font=ctk.CTkFont(size= 30, weight="bold"))
tittle_label.pack(pady=25)

# App dashboard
menu_text = ctk.CTkTextbox(info, width= 700, height= 400)
menu_text.configure(fg_color = "#ffffff", text_color = "#000000")
menu_text.pack(fill = "y", pady = 20)


def open_menu(): 
    menu_text.delete("0.0", "end")
    for objective in user.plan: # To go through all objectives 
        progress = objective.view_progression() # To get objective progression
        report = "FINALISED!" if progress >= 100 else f"{progress:.1f}%" # Shows "Finalized" if user has completed the objective if not, shows the current progression in %
        menu_text.insert("end", f"{objective.topic} : {objective.hours_accomplished}h/{objective.expected_hours}h | {report}\n") # Objective line in dashboard 


def insert_objective():
    def send():
        topic = insert_topic.get() # For the user to input the objective topic
        try: 
            expected_hours = float(insert_hours.get()) # To convert the objective expected hours into float
            due_date = datetime.datetime.strptime(insert_date.get(), "%Y-%m-%d").date() # On which date the user is willing to complete the objective
        except ValueError:
            messagebox.showerror("Invalid data", "Please insert a valid data") # In case the user enters incorrect data  
            return
        
        objective = Obj(topic, expected_hours, due_date) 
        user.put_objective(objective) # To add user objective to dashboard list
        open_menu()
        messagebox.showinfo("Your objective was placed successfully!") 
        popup.destroy # To close the window that pop's up

    # New objective layout
    popup = ctk.CTkToplevel(planner)
    popup.title ("New objective")
    popup.geometry("500x400")

    # For user to insert the objective topic
    ctk.CTkLabel(popup, text="Topic: ", font=ctk.CTkFont(weight="bold")).pack(pady=(20,0)) # Topic design
    insert_topic = ctk.CTkEntry(popup, width= 400)
    insert_topic.pack()

    # For user to insert the expected hours of the objective
    ctk.CTkLabel(popup, text="Expected Hours:", font=ctk.CTkFont(weight="bold")).pack(pady=(20,0)) # Expected hours design
    insert_hours = ctk.CTkEntry(popup, width= 400)
    insert_hours.pack()
    
    # For user to insert the due date of the object
    ctk.CTkLabel(popup, text="Due date (YYYY-MM-DD):", font=ctk.CTkFont(weight="bold")).pack(pady=(20,0)) # DUe date design
    insert_date = ctk.CTkEntry(popup, width= 400)
    insert_date.pack()

    # To send objective details (Send button)
    ctk.CTkButton(popup, text= "Add Objective", command= send, font=ctk.CTkFont(size = 12, weight= "bold", slant= "italic")).pack(pady = 30)


def log_objective():
    if not user.plan:
        messagebox.showwarning("Currently, there are no objectives","Add a objective first") # In case if the user has not added any objectives
        return  

    def send(): 
        selected_topic = option_menu.get()
        selected_obj = [obj for obj in user.plan if obj.topic == selected_topic] # To find the chosen objective by the user
        if not selected_obj:
            messagebox.showwarning("The selected objective was not found") # In case if the chosen objective is not found
            return

        try: 
            expected_hours = float(insert_hours.get())
        except ValueError:
            messagebox.showerror("Please insert a valid number of hours!") # In case the user enters incorrect data 
            return
        
        selected_obj[0].track_time(expected_hours) # Update the objective using current logged time by the user
        open_menu()
        messagebox.showinfo("Your completed hours were placed successfully") # Confirmation
        popup.destroy()

    popup = ctk.CTkToplevel(planner)
    popup.title ("Loggin time in hours")
    popup.geometry("500x400")

    # To go through objectives list
    ctk.CTkLabel(popup, text = "Choose topic:", font=ctk.CTkFont(weight="bold")).pack(pady=(10,0)) # "Choose Topic" design
    option_menu = ctk.CTkOptionMenu(popup, values=[obj.topic for obj in user.plan])
    option_menu.pack(pady=(0,20))

    # For user to insert the completed hours 
    ctk.CTkLabel(popup, text = "Completed hours so far:", font=ctk.CTkFont(weight="bold")).pack(pady=(20,0)) # "Completed hours" design
    insert_hours = ctk.CTkEntry(popup, width= 400)
    insert_hours.pack()

    # Submit button
    ctk.CTkButton(popup, text = "Record time", command=send, font=ctk.CTkFont(size = 12, weight= "bold", slant = "italic")).pack(pady=30) # "Record time" button design


def display_status():
    if not user.plan:        
        messagebox.showinfo("There is currently no data available" ,"Add a objective first" ) # Pop's up when there are no objectives available 
        return

    # Creation of objective record 
    progress_record = ctk.CTkToplevel(planner)
    progress_record.title("Objective record")
    progress_record.geometry("600x500")

    frame = ctk.CTkScrollableFrame(progress_record, width= 500, height = 400 ) # For user to be able to scroll through objectives
    frame.pack(pady =10, padx = 10)

    # To loop through all objectives (tittle: expected hours and completed hours) 
    for obj in user.plan: 
        ctk.CTkLabel(frame, text =f" {obj.topic}", font=ctk.CTkFont(size= 18, weight="bold")).pack(anchor ="center", padx = 20, pady = (20,0))
        ctk.CTkLabel(frame, text = f" Expected hours: {obj.expected_hours}h").pack(anchor ="center", padx = 20, pady = (20,0))
        ctk.CTkLabel(frame, text= f" Completed hours so far: {obj.hours_accomplished}h").pack(anchor ="center",padx = 20, pady = (20,0))

        if obj.history: 
            for date, hrs in obj.history: 
                ctk.CTkLabel(frame, text=f"{date} - {hrs}h").pack(anchor = "center", padx = 40) # Will also show up in case if the user logged the time 

        # Will show up in case if the user did not log the completed hours 
        else: 
            ctk.CTkLabel(frame, text= "(No hours were recorded so far)", font=ctk.CTkFont(size = 13, slant= "italic")).pack(anchor = "center", padx = 40)


# To clear all objectives
def clear_goals():
    user.plan.clear()
    save_person(user) # To save after clearance  
    open_menu()
    messagebox.showinfo("All topics were cleared successfully")


menu_text.insert("0.0", "Greetings from your planner")
open_menu()
planner.mainloop() 