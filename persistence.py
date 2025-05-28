import pickle
import os

DATA_FILE = "person_data.pkl"

def save_person(person):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(person, f)
