from errors import DateError, TimeError
from manual_input import ManualInput
from tracker_cls import Tracker, TrackingMode
from datetime import date, time
import sys
from colorama import init

# Features to implement:
# When the user starts an activity, start a timer in the UI 
# Sound a beep when you start 
# Provide an option to work via pomodoros or freestyle 
# A pomodoro could be of variable length
# If this is the first time an activty is tracked, the user should specify a minimum number of hours to do it per day. 

def main():
    init(autoreset=True)
    activity = input("Activity to track: ")
    tracker = Tracker(activity)
    data = tracker.read_from_memory()
    print(data)
    choosen_mode = tracker.get_mode()
    if choosen_mode == TrackingMode.AUTOMATIC:
        tracker.start_session()

    elif choosen_mode == TrackingMode.MANUAL:

        while True:
            input_date = input("Date (YYYY-MM-DD): ")
            input_start = input("When did you start? (HH:MM:SS) ")
            input_end = input("When did you finish? (HH:MM:SS) ")
            try:
                user_input = ManualInput(date = input_date, start=input_start , end=input_end)
                user_input.write_to_memory(file_path=tracker.file_path)
                break
            except DateError as e:
                print(e.message)
            except TimeError as e: 
                print(e.message)
    else:
        sys.exit("Something went wrong. Invalid input")

if __name__ == "__main__":
    main()



