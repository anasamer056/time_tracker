import csv
import datetime
from errors import DateError, TimeError
from datetime import date, time, datetime

class ManualInput:
    def __init__(self, date, start, end) -> None:
        self.date = date
        self.start = start
        self.end = end

    @property 
    def date(self):
        return self._date
    
    @date.setter
    def date(self, d):
        try: 
            self._date = datetime.strptime(d, "%m-%d").replace(year=date.today().year).date()	
        except ValueError:
            raise DateError
    
    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, s):
        try: 
            self._start = time.fromisoformat(s)	
        except ValueError:
            raise TimeError    
        
    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, e):
        try: 
            self._end = time.fromisoformat(e)	
        except ValueError:
            raise TimeError  
        
    def write_to_memory(self, file_path): 
        with open(file_path, "a") as file: 
            writer = csv.DictWriter(file, fieldnames= ["date", "start", "end"])
            writer.writerow({"date": self.date, "start": self.start, "end": self.end})  

    