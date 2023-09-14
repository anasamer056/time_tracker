class DateError(ValueError):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)
    
class TimeError(ValueError):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

