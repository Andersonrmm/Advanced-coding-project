import datetime

class Obj: 
    def __init__(self, topic, expected_hours, due_date):
        self.topic = topic # Name of the objective to be completed
        self.expected_hours = expected_hours # How many hours needed for the objective to be completed 
        self.due_date = due_date 
        self.hours_accomplished = 0 # The total amount of the hours done so far
        self.history = [] # keeps a record of the dates and hours 

    def track_time(self, hours):
        self.hours_accomplished += hours
        self.history.append((datetime.date.today(), hours)) # Log with the present date and the hours worked

    def view_progression(self): 
        return (self.hours_accomplished / self.expected_hours) * 100 # To calculate the percentage completed of the objective
    