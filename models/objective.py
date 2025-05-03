import datetime

class objective: 
    def __init__(self, topic, goal_duration, due_date):
        self.topic = topic
        self.goal_duration = goal_duration
        self.due_date = due_date 
        self.hours_accomplished = 0
        self.history = []

    def track_time(self, hours):
        self.hours_accomplished += hours
        self.history.append((datetime.date.today(), hours))

    def view_progression(self): 
        return (self.hours_accomplished / self.goal_duration) * 100
    