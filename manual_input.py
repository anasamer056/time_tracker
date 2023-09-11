import csv
import datetime
from errors import DateError, TimeError
from datetime import date, time, datetime

class ManualInput:
    def __init__(self, date, work, relax='0') -> None:
        self.date = date
        self.work = work
        self.relax = relax

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
    def work(self):
        return self._work

    @work.setter
    def work(self, s):
        try: 
            self._work = int(s)	
        except ValueError:
            raise TimeError    
        
    @property
    def relax(self):
        return self._relax

    @relax.setter
    def relax(self, e):
        try: 
            self._relax = int(e)	
        except ValueError:
            raise TimeError  
        
    def write_to_memory(self, file_path): 
        with open(file_path, "a") as file: 
            writer = csv.DictWriter(file, fieldnames= ["date", "work", "relax"])
            writer.writerow({"date": self.date, "work": self.work, "relax": self.relax})  

    