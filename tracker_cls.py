import os.path
import csv

class Tracker:

    #### Attributes: 
    # Activity name
    def __init__(self, activity):
        self.activity = activity


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
    
    # Writes the activity name to memory
    def create_file(self):
        file_name = f"data/{self.activity}.csv"
        with open(file_name, "x") as file:
           pass 
            
            
        
        
    # If {activity} is not in memory, it creates it and returns an empty list. Otherwise it reads it
    def read_from_memory(self):
        file_name = f"data/{self.activity}.csv"
        try:
            self.create_file() 
        except FileExistsError:
            print("went down the reading path") 
            with open(file_name, "r") as file:
                reader = csv.DictReader(file)
                data = []
                for row in reader:
                    data.append(row)
                return data 
        else: 
            print("went down the creation path")
            with open(file_name, "w") as file: 
                writer = csv.writer(file)
                writer.writerow(["date", "start", "end"])
                return []
