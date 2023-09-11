from datetime import timedelta

class Stats:
    
    def __init__(self, activity):
        self.activity = activity
        self._file_path = f"data/{activity}_stats.csv"
        self._streak = 0
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
        
    def read_from_memory(self):
        pass
    
    def write_to_memory(self):
        pass
    
    def get_streak(self, clean_data: list):
        days = []

        days = list(map(lambda row: row["date"], clean_data))
        
        streak = 1 if len(days) > 0  else 0

        for i in range(len(days) - 1):
            if days[i+1] - days[i] == timedelta(days=1):
                streak += 1
            else:
                streak = 1
                
        return streak
        
