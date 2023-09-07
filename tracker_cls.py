import os.path
import csv

class Tracker:

    #### Attributes: 
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
