"""
Time

A basic time class. Uses 24-hour time unless changed.
"""

class Time:
    # Defines and initializes the variables of the class
    def __init__(self, hour, minute, second):
        self.hour   = hour
        self.minute = minute
        self.second = second

    # Displays a time in the 12-hour format
    def display12(self):
        # display AM or PM?
        isPM = False
        if self.hour > 11:
            isPM = True
        
        # change 24 hour time to 12
        tempHour = self.hour
        if self.hour == 0:
            tempHour = 12
        elif self.hour > 12:
            tempHour -= 12
        
        # create string copies with leading zeros, if necessary
        strHour = str(tempHour).zfill(2)
        strMin  = str(self.minute).zfill(2)
        strSec  = str(self.second).zfill(2)

        # get everything ready to print
        timeOutput = (strHour + ":" 
                    + strMin + ":"
                    + strSec)

        # append AM or PM
        if isPM == True:
            timeOutput += " PM"
        else:
            timeOutput += " AM"

        # display the 12-hour time
        print(timeOutput)

    # Displays a time in the 24-hour format
    def display24(self):
        # create string copies with leading zeros, if necessary
        strHour = str(self.hour).zfill(2)
        strMin  = str(self.minute).zfill(2)
        strSec  = str(self.second).zfill(2)

        # get everything ready to print
        timeOutput = (strHour + ":" 
                    + strMin + ":"
                    + strSec)

        # display the 24-hour time
        print(timeOutput)