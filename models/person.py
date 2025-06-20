class Person:
    def __init__(self, person_id, name):
        self.person_id = person_id
        self.name = name

class User(Person):
    def __init__(self, person_id, name):
        super().__init__(person_id, name) # For user class to reuse the code from person class 
        self.plan = []

    def put_objective(self,objective):
        self.plan.append(objective) # To add the plan to the given plans list  