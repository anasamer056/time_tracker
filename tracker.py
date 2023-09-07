from tracker_cls import Tracker

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
    print(data)
    


if __name__ == "__main__":
    main()



