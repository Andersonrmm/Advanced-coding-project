import pickle
import os

DATA_FILE = "person_data.pkl"

def save_person(person):
    with open(DATA_FILE, "wb") as f: # To open the file in wb (write binary) mode 
        pickle.dump(person, f) # Converts the person object and saves it to the file

def read_person():
    if os.path.exists(DATA_FILE): # Sees if the file is existent.
        with open(DATA_FILE, "rb") as f: # To open the file in rb (read binary) mode
            return pickle.load(f) # Takes the object from the file, breaks it down, and returns it.
    return None
