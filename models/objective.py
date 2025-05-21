import datetime

class objective: 
    def __init__(self, topic, objective_duration, due_date):
        self.topic = topic # Name of the objective to be completed
        self.expected_hours = objective_duration # How many hours needed for the objective to be completed 
        self.due_date = due_date 
        self.hours_accomplished = 0 # The total amount of the hours done so far
        self.history = [] # keeps a record of the dates and hours 

    def track_time(self, hours):
        self.hours_accomplished += hours
        self.history.append((datetime.date.today(), hours)) # Log with the present date and the hours worked

    def view_progression(self): 
        return (self.hours_accomplished / self.objective_duration) * 100 # To calculate the percentage completed of the objective
    