class person:
    def __init__(self, person_id, name):
        self.person_id = person_id
        self.name = name

class user(person):
    def __init__(self, person_id, name):
        person.__init__(self, person_id, name)
        self.plan = []

    