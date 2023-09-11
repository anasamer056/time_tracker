from errors import DateError, TimeError
from manual_input import ManualInput
from tracker_cls import Tracker, TrackingMode
from stats import Stats
from datetime import date, time
import sys
from colorama import init

#^ Features to implement:
# Sound a beep when you start 
# If this is the first time an activty is tracked, the user should specify a minimum number of hours to do it per day. 
# Provide stats like the current streak, total hours of work and rest, 

#! Bugs
# Test and fix the manual mode 
# Sort the array before cleaning it up 
# Write it to memory again after cleaning it up
# Revert back to minutes instead of seconds

#& Refactor
# Add attributes for the data inside the Tracker class instead of pass it as an argument
# Call Tracker.read_from_memory() in __init__() and store the clean data as an attribute 
# Move all the printing to main.py
# Create a sparate folder for each activity to store the data and stats together

def main():
    init(autoreset=True)

    activity = input("Activity to track: ")
    tracker = Tracker(activity)
    
    clean_data = tracker.read_from_memory()
    stats = Stats(activity, clean_data)
    print("data: ", clean_data)
    print("stats: ", [stats.streak, stats.longest_streak, stats.total_work, stats.total_relax])
    choosen_mode = tracker.get_mode()
    if choosen_mode == TrackingMode.AUTOMATIC:
        tracker.start_session()

    elif choosen_mode == TrackingMode.MANUAL:

        while True:
            input_date = input("Date (YYYY-MM-DD): ")
            input_work = input("How many minutes did you work? ")
            try:
                user_input = ManualInput(input_date, input_work)
                user_input.write_to_memory(tracker.file_path)
                break
            except DateError as e:
                print(e.message)
            except TimeError as e: 
                print(e.message)
    else:
        sys.exit("Something went wrong. Invalid input")

if __name__ == "__main__":
    main()



