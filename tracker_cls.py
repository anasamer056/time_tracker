import os.path
import csv
from enum import Enum

class Tracker:

    ### Attributes: 
    # Activity name
    def __init__(self, activity):
        self.activity = activity
        self._file_path = f"data/{self.activity}.csv"

    # Activtiy setter and getter 
    @property 
    def activity(self):
        return self._activity
    
    @activity.setter
    def activity(self, a: str):
        if a: 
            self._activity = a.lower().strip()
        else: 
            raise ValueError("Activity name cannot be empty")
    
    # file_path getter
    @property
    def file_path(self):
        return self._file_path

    # Writes the activity name to memory
    def create_file(self):
        with open(self.file_path, "x") as file:
           pass         
        
    # If {activity} is not in memory, it creates it and returns an empty list. Otherwise it reads it
    def read_from_memory(self):
        try:
            self.create_file() 
        except FileExistsError:
            print("went down the reading path") 
            with open(self.file_path, "r") as file:
                reader = csv.DictReader(file)
                data = []
                for row in reader:
                    data.append(row)
                return data 
        else: 
            print("went down the creation path")
            with open(self.file_path, "w") as file: 
                writer = csv.writer(file)
                writer.writerow(["date", "start", "end"])
                return []

    # Gets the mode, either Auto or Manual 
    @staticmethod
    def get_mode():
        while True:
            try:
                choosen_mode = int(input((
                    "\nChoose your preferred mode:\n"
                    "1) Let the app do the tracking\n"
                    "2) Insert the data manually\n"
                    "Choice: " 
                    )))
            except ValueError: 
                print("Please type a number, either 1 or 2")
                continue
            else: 
                if choosen_mode not in range(1, 3):
                    print("Please type a number, either 1 or 2")
                    continue
                return TrackingMode(choosen_mode)

    # Starts an activity session
    def start_session(self):
        pass

class TrackingMode(Enum):
    AUTOMATIC = 1
    MANUAL = 2