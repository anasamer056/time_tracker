from tracker_cls import Tracker, TrackingMode
import sys

# Features to implement:
# Track more than one activity 
# Store data in a separate file for each activity
# When the user starts an activity, start a timer in the UI 
# Sound a beep when you start 
# Provide an option to work via pomodoros or freestyle 
# A pomodoro could be of variable length
# If this is the first time an activty is tracked, the user should specify a minimum number of hours to do it per day. 

def main(): 
    activity = input("Activity to track: ")
    tracker = Tracker(activity)
    data = tracker.read_from_memory()
    choosen_mode = tracker.get_mode()
    if choosen_mode == TrackingMode.AUTOMATIC:
        # tracker.start_session()
        pass
    elif choosen_mode == TrackingMode.MANUAL:
        # tracker.write_to_memory()
        pass
    else:
        sys.exit("Something went wrong. Invalid input")




if __name__ == "__main__":
    main()



