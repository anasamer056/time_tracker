from datetime import timedelta
import os 
import csv 

class Stats:
    
    headers = ["streak", "longest streak", "total work", "total relax"]
    
    def __init__(self, activity, clean_data):
        self.activity = activity
        self._clean_data = clean_data
        self._file_path = f"data/{activity}_stats.csv"
        self._streak = 0
        self._longest_streak = 0
        self._total_work = 0
        self._total_relax = 0

        # Intialize the attributes from memory
        self.read_from_memory()

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
    def clean_data(self):
        return self._clean_data

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
        try:
            if not os.path.exists("data/"):
                os.mkdir("data/")
            with open(self.file_path, 'x') as _:
                pass

        except FileExistsError: 
            # Reading logic
            with open(self.file_path, 'r') as file: 
                reader = csv.DictReader(file, fieldnames = self.headers)
                for row in reader:
                    self._streak = row["streak"]
                    self._longest_streak = row["longest streak"]
                    self._total_work = row["total work"]
                    self._total_relax = row["total relax"]
    
        else: 
            # Write for the first time
            with open(self.file_path, 'w') as file:
                writer = csv.DictWriter(file, fieldnames = self.headers)
                writer.writeheader()
            
    
    def write_to_memory(self):
        # Update the attributes
        self._streak = self.get_streak()
        self_longest_streak = self.streak if self.streak > self.longest_streak else self.logest_strek
        self._total_work, self._total_relax = self.get_total_work_and_relax()

        with open(self.file_path, 'w') as file:
            writer = csv.DictWriter(file, fieldnames = self.headers)
            writer.writeheader()
            to_write = {
                    "streak": self.streak,
                    "longest streak": self.longest_streak,
                    "total work": self.total_work,
                    "total relax": self.total_relax,
                    }
            writer.writerow(to_write)

    def get_streak(self):
        days = list(map(lambda row: row["date"], self.clean_data))
        streak = 1 if len(days) > 0  else 0

        for i in range(len(days) - 1):
            if days[i+1] - days[i] == timedelta(days=1):
                streak += 1
            else:
                streak = 1
        
        return streak
    
    def get_total_work_and_relax(self):
        
        t_work = 0
        t_relax = 0
        
        for row in self.clean_data:
            t_work += row["work"]
            t_relax += row["relax"]
        
        return (t_work, t_relax)
        
        
