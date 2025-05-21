import datetime

def display_menu(person):
    print(f"\n Menu for {person}")
    for objective in person.objective:
        progress = objective.get_progress()
        report = "Finalized" if progress >= 100 else f"{progress:.1f}% complete"
        print(f"- {objective.topic}: {objective.hours_accomplished}/{objective.expected_hours}h ({report})") 

def insert_objective(person, objective):
    topic = input("Topic of your objective:")
    hours = float(input("Expected hours:"))
    due_date_str = input("Due date as (Day(DD)-Month(MM)-Year(YYYY):")
    due_date = datetime.datetime.strptime(due_date_str, "%d-%m-%y").date()
    objective = objective(topic, hours, due_date)
    person.insert_objective(objective)
    print("Objective added!")