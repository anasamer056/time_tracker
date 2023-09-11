import os.path
import csv
from enum import Enum
import time
import threading
from datetime import date
from colorama import Fore, Back, Style


class TrackingMode(Enum):
    AUTOMATIC = 1
    MANUAL = 2

class TimerType(Enum):
    SESSION = "session"
    SHORT_BREAK = "short break"
    LONG_BREAK = "long break"

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
        if not os.path.exists("data/"):
            os.mkdir("data/")
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
                    day = date.fromisoformat(row["date"])
                    work = int(row["work"])
                    relax = int(row["relax"])
                    data.append({"date": day, "work": work, "relax": relax})
                unique_days = self.get_unique_days(data)
                clean_data = self.cleanup(unique_days, data)
                return clean_data
        else: 
            print("went down the creation path")
            with open(self.file_path, "w") as file: 
                writer = csv.writer(file)
                writer.writerow(["date", "work", "relax"])
                return []

    # Writes the date, work, relax to memory
    def write_to_memory(self, date, work, relax):
        with open(self.file_path, "a") as file:
            writer = csv.DictWriter(file, fieldnames= ["date", "work", "relax"])
            writer.writerow({"date": date, "work": work, "relax": relax})  
    
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
        
        session_time = 0
        short_break_time = 0
        long_break_time = 0

        # Getting the time values 
        while True:
            try:
                print("")
                session_time = int(input("Session duration: (In numeral minutes. e.g. 25, 40) "))
                short_break_time = int(input("Short break: "))
                long_break_time = int(input("Long break: "))
                print("")
                break
            except ValueError: 
                print("Invalid input. Pick a number")
                continue

        # Thread events to control the flow
        stop_event = threading.Event()  # Event to signal when to stop the timer
        pause_event = threading.Event()  # Event to signal when to pause the timer
               
        handler_thread = threading.Thread(target=self.pomodoro_handler, args=(session_time, stop_event, pause_event), daemon=True)
        handler_thread.start()
        time.sleep(0.1)

        for i in range (1,4):
            self.timer(session_time, stop_event, pause_event, TimerType.SESSION, session_num=i)
            self.timer(short_break_time, stop_event, pause_event,TimerType.SHORT_BREAK,True)
    
        self.timer(session_time, stop_event, pause_event, TimerType.SESSION, session_num=4)
        self.timer(long_break_time, stop_event, pause_event, TimerType.LONG_BREAK, True, )

        
    def pomodoro_handler(self, total_time, stop_event, pause_event):
        while True:
            user_input = input(f"Enter {Fore.MAGENTA}'s' {Fore.RESET}to stop, {Fore.MAGENTA}'p' {Fore.RESET}to pause/unpause. \n\n")
            if user_input == 's':
                stop_event.set()  # Set the stop event to signal the timer to stop
                break
            elif user_input == 'p':
                if pause_event.is_set():
                    print("Timer resumed.")
                    pause_event.clear()  # Clear the pause event to resume the timer
                else:
                    print("Timer paused.")
                    pause_event.set()  # Set the pause event to pause the timer
            

    def timer(self, minutes: int, stop_event: threading.Event, pause_event, timer_type: TimerType, is_break: bool = False, session_num = 0):
        # seconds = minutes * 60
        seconds = minutes

        if stop_event.is_set():
            return
        
        if timer_type == TimerType.SESSION:
            print(Fore.LIGHTGREEN_EX + f"Started {timer_type.value} #{session_num}                  ")
        else: 
            print(Fore.LIGHTGREEN_EX + f"Started {timer_type.value}                  ")
        
        while seconds:
            if stop_event.is_set():
                break  # Exit the timer loop if the stop event is set
            if not pause_event.is_set():
                mins, secs = divmod(seconds, 60)
                timer = Fore.YELLOW + f"{mins:02d}:{secs:02d}".center(20)
                print(timer, end='\r')
                time.sleep(1)
                seconds -= 1

        if not stop_event.is_set(): # Finished the countdown without stopping, so now we can write to memory
            if is_break:
                self.write_to_memory(date.today(), 0, max(1, round(minutes/60, 2)))
            else:
                self.write_to_memory(date.today(), max(1, round(minutes/60, 2)), 0)
            
    def get_unique_days(self, data: list):
        
        unique_days = []
        
        for item in data:
            if item["date"] not in unique_days: 
                unique_days.append(item["date"])

        return unique_days
        
    def cleanup(self, unique_days: list, sorted_data: list):
        clean_data = []
        for i in range(len(unique_days)):
            clean_data.append({"date": unique_days[i], "work": 0, "relax": 0})
            for j in range(len(sorted_data)):
                if sorted_data[j]["date"] == unique_days[i]:
                    clean_data[i]["work"] += sorted_data[j]["work"]
                    clean_data[i]["relax"] += sorted_data[j]["relax"]
        
        return clean_data
        


