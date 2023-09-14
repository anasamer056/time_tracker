from errors import DateError, TimeError
from manual_input import ManualInput
from tracker_cls import Tracker, TrackingMode
from stats import Stats
from datetime import date, time
import sys
from colorama import init, Fore
from tabulate import tabulate #type: ignore


#! Bugs
# Revert back to minutes instead of seconds

#& Refactor
# Add attributes for the data inside the Tracker class instead of pass it as an argument
# Call Tracker.read_from_memory() in __init__() and store the clean data as an attribute 
# Move all the printing to main.py
# Create a sparate folder for each activity to store the data and stats together
# Rename "relax" to "rest"

def main():
    init(autoreset=True)

    activity = input("Activity to track: ")
    tracker = Tracker(activity)
    
    clean_data = tracker.read_from_memory()
    stats = Stats(activity, clean_data)
    stats_table = [{
        Fore.YELLOW + "Current Streak": stats.streak, 
        "Longest Streak": stats.longest_streak,
        "Total Work Time": stats.total_work, 
        "Total Break Time" + Fore.RESET :stats.total_relax,
        }]

    print(tabulate(stats_table, headers="keys", tablefmt="pretty"))
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



