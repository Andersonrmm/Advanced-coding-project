import datetime

def display_menu(person):
    print(f"\n Menu for {person}")
    for objective in person.objective:
        progress = objective.get_progress()
        report = "Finalized" if progress >= 100 else f"{progress:.1f}% complete"
        print(f"- {objective.topic}: {objective.hours_accomplished}/{objective.expected_hours}h ({report})") 

