class DateError(ValueError):
    def __init__(self, message="Date isn't in ISO format (YYYY-MM-DD)"):
        self.message = message
        super().__init__(self.message)
    
class TimeError(ValueError):
    def __init__(self, message="Time isn't in ISO format (HH:[MM]:[SS])"):
        self.message = message
        super().__init__(self.message)

