import os.path
import csv
from enum import Enum
import time
import threading
from datetime import date

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
                    day = date.fromisoformat(row["date"])
                    start = int(row["start"])
                    end = int(row["end"])
                    data.append({"date": day, "start": start, "end": end})
                unique_days = self.get_unique_days(data)
                clean_data = self.cleanup(unique_days, data)
                return clean_data
        else: 
            print("went down the creation path")
            with open(self.file_path, "w") as file: 
                writer = csv.writer(file)
                writer.writerow(["date", "start", "end"])
                return []

    # Writes the date, start, end to memory
    def write_to_memory(self, date, start, end):
        with open(self.file_path, "a") as file:
            writer = csv.DictWriter(file, fieldnames= ["date", "start", "end"])
            writer.writerow({"date": date, "start": start, "end": end})  
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
        
        total_time = 0
        break_time = 0
        long_break_time = 0

        # Getting the time values 
        while True:
            try:
                total_time = int(input("Session duration: (In numeral minutes. e.g. 25, 40) "))
                break_time = int(input("Short break: "))
                long_break_time = int(input("Long break: "))
                break
            except ValueError: 
                continue

        # Thread events to control the flow
        stop_event = threading.Event()  # Event to signal when to stop the timer
        pause_event = threading.Event()  # Event to signal when to pause the timer
        
        # Declaring threads for the main session, short break, and long break
       
        handler_thread = threading.Thread(target=self.pomodoro_handler, args=(total_time, stop_event, pause_event), daemon=True)
        
        # Starting the sessions
        handler_thread.start()

        for i in range (1,4):
            if not stop_event.is_set():

                pomodoro_thread = threading.Thread(target=self.pomodoro_timer, args=(total_time, stop_event, pause_event), daemon=True) 
                break_thread = threading.Thread(target=self.pomodoro_timer, args=(break_time, stop_event, pause_event, True), daemon=True)
 
                print(f"\nSession #{i}\n")
                pomodoro_thread.start()  # Start the Pomodoro timer thread
                pomodoro_thread.join()
                print("\nShort break\n")
                break_thread.start()
                break_thread.join()
 
        if not stop_event.is_set():
            pomodoro_thread = threading.Thread(target=self.pomodoro_timer, args=(total_time, stop_event, pause_event), daemon=True)

            print("\n4th Session\n")
            pomodoro_thread.start()
            pomodoro_thread.join()
            
            print("\nLong break\n")
            long_break_thread = threading.Thread(target=self.pomodoro_timer, args=(long_break_time, stop_event, pause_event, True), daemon=True)
 
            long_break_thread.start()
            long_break_thread.join()
        

    def pomodoro_handler(self, total_time, stop_event, pause_event):
        while True:
            user_input = input("Enter 's' to stop, 'p' to pause/unpause, or 'r' to reset: ")
            print("\n")
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
            elif user_input == 'r':
                stop_event.set()  # Set the stop event to stop the current timer
                time.sleep(1) # Giving downtime for the complier to go to the timer thread.
                stop_event.clear()  # Defensive cleanup to start the new timer on a clean slate.
                pause_event.clear()  

                pomodoro_thread = threading.Thread(target=self.pomodoro_timer, args=(total_time, stop_event, pause_event), daemon=True)
                pomodoro_thread.start()  # Start a new Pomodoro timer thread


    
    def pomodoro_timer(self, minutes: int, stop_event: threading.Event, pause_event, is_break: bool = False):
        # seconds = minutes * 60
        seconds = minutes
        while seconds:
            if stop_event.is_set():
                break  # Exit the timer loop if the stop event is set
            if not pause_event.is_set():
                mins, secs = divmod(seconds, 60)
                timer = f"{mins:02d}:{secs:02d}".center(60)
                
                print(timer, end='\r')
                time.sleep(1)
                seconds -= 1
            else:
                time.sleep(1)
        if not stop_event.is_set(): # Finished the countdown without stopping, so now we can write to memory
            if is_break:
                self.write_to_memory(date.today(), 0, round(minutes/60, 2))
            else:
                self.write_to_memory(date.today(), round(minutes/60, 2), 0)
            
    def get_unique_days(self, data: list):
        
        unique_days = []
        
        
        for item in data:
            if item["date"] not in unique_days: 
                unique_days.append(item["date"])

        return unique_days
        


    def cleanup(self, unique_days: list, sorted_data: list):
        clean_data = []
        for i in range(len(unique_days)):
            clean_data.append({"date": unique_days[i], "start": 0, "end": 0})
            for j in range(len(sorted_data)):
                if sorted_data[j]["date"] == unique_days[i]:
                    clean_data[i]["start"] += sorted_data[j]["start"]
                    clean_data[i]["end"] += sorted_data[j]["end"]

        
        return clean_data
        


class TrackingMode(Enum):
    AUTOMATIC = 1
    MANUAL = 2
