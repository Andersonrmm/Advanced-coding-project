import datetime
class objective: 
    def __init__(self, topic, goal_duration, due_date):
        self.topic = topic
        self.goal_duration = goal_duration
        self.due_date = due_date 
        self.hours_accomplished = 0
        self.history = []