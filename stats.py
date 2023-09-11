from datetime import timedelta
import os 
import csv 

class Stats:
    
    def __init__(self, activity):
        self.activity = activity
        self._file_path = f"data/{activity}_stats.csv"
        self._streak = 0
        self._longest_streak = 0
        self._total_work = 0
        self._total_relax = 0

    @property
    def activity(self):
        return self._activity
    
    @activity.setter
    def activity(self, a):
        if a:
            self._activity = a
        else: 
            raise ValueError("Activity name cannot be empty")
    
    @property
    def file_path(self):
        return self._file_path

    @property
    def streak(self):
        return self._streak
    
    @property
    def longest_streak(self):
        return self._longest_streak

    @property
    def total_work(self):
        return self._total_work
    
    @property
    def total_relax(self):
        return self._total_relax
        
    def read_from_memory(self):
        headers = ["streak", "longest streak", "total work", "total relax"]
        try:
            if not os.path.exists("data/"):
                os.mkdir("data/")
            with open(self.file_path, 'x') as _:
                pass

        except FileExistsError: 
            # Reading logic
            with open(self.file_path, 'r') as file: 
                reader = csv.DictReader(file, fieldnames = headers)
                for row in reader:
                    self._streak = row["streak"]
                    self._longest_streak = row["longest streak"]
                    self._total_work = row["total work"]
                    self._total_relax = row["total relax"]
    
        else: 
            # Write for the first time
            with open(self.file_path, 'w') as file:
                writer = csv.DictWriter(file, fieldnames = headers)
                writer.writeheader()
            
    
    def write_to_memory(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'x'):
                return
        else: 
            #! TODO
            pass
    
    def get_streak(self, clean_data: list):
        days = list(map(lambda row: row["date"], clean_data))
        streak = 1 if len(days) > 0  else 0

        for i in range(len(days) - 1):
            if days[i+1] - days[i] == timedelta(days=1):
                streak += 1
            else:
                streak = 1
                
        return streak

    
        
