class person:
    def __init__(self, person_id, name):
        self.person_id = person_id
        self.name = name

class user(person):
    def __init__(self, person_id, name):
        person.__init__(self, person_id, name) # For user class to reuse the code from person class 
        self.plan = []

    def put_plan(self,plan):
        self.plans.append(plan) # To add the plan to the given plans list  