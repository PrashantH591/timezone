"""
Time Zone Converter

This program will allow the user to convert a date and a time
to another time zone.
"""

# give access to the Time class 
from timeClass import Time

# allows user to use their current time in one step
import datetime


"""
Display Time Zones, "Option A"

This will display the time zones available for conversion.
"""
def displayTimeZones(listTimeZones):
    # reread the file in case the user added a time zone 
    readTimeZones(listTimeZones)

    # header for the table
    print("Default Time Zones\n")
    print("CITY: \t\t\tUTC:")

    # present the default times
    timeZone = str("")
    for i in range(len(listTimeZones)):
        # prints if we're using any custom time zones
        if (i == 63):
            print("\nCustom Time Zones\n")
            print("CITY: \t\t\tUTC:")

        # cities start the string
        if i % 2 == 0:
            timeZone += listTimeZones[i]
            i += 1

        # UTCs end the string, string is printed, then reset 
        else:
            timeZone += "\t"
            if len(listTimeZones[i - 1]) <= 15:
                timeZone += "\t"
            timeZone += listTimeZones[i]

            print(timeZone)
            timeZone = str("")


"""
Convert Time, "Option B"

This converts the user's time zone into another of their choice
and displays it.
"""
def convertTime(listTimeZones):
    # allows user to continue using this function until finished
    doLoop = True
    while doLoop == True:
        # gets the user's time
        userTime = getUserTime()

        # display the time zones
        displayTimeZones(listTimeZones)

        # get the user's own time zone
        reprompt = True
        while reprompt == True:
            strGetTZ = "Your time zone (UTC): "
            userTZ = float(input("\n" + strGetTZ))

            # user is reprompted if the time zone is invalid
            if isValidTimeZone(userTZ, listTimeZones):
                reprompt = False
            else:
                print("\nPlease enter a valid UTC.")

        # ask which they'd like to change it to
        reprompt = True
        while reprompt == True:
            strGetTZ = "Destination time zone (UTC): "
            newTZ = float(input("\n" + strGetTZ))

            # user is reprompted if the time zone is invalid
            if isValidTimeZone(newTZ, listTimeZones):
                reprompt = False
            else:
                print("\nPlease enter a valid UTC.")

        # find the time difference in hours and minutes, if needed
        diffHour = newTZ - userTZ
        diffMinutes = diffHour - int(diffHour)
        diffMinutes = int(diffMinutes * 60)
        diffHour = int(diffHour)

        # account for odd time zones changing minutes into hours
        newHour = userTime.hour + diffHour
        newMinute = userTime.minute + diffMinutes
        if newMinute < 0:
            newHour -= 1
            newMinute += 60
        elif newMinute > 59:
            newHour += 1
            newMinute -= 60

        # account for a change in day
        day = ""
        if newHour < 0:
            newHour += 24
            day = "Yesterday"
        elif newHour > 23:
            newHour -= 24
            day = "Tomorrow"
        else:
            day = "Today"

        # create a Time object from the data
        newTime = Time(newHour, newMinute, userTime.second)

        # find the corresponding cities
        userResult = "\nYour Time ({}):"
        destResult = "\nDestination Time ({}):"
        userCity = ""
        destCity = ""
        for i in range(len(listTimeZones)):
            if i % 2 != 0:
                if float(listTimeZones[i]) == userTZ:
                    userCity = listTimeZones[i - 1]
                if float(listTimeZones[i]) == newTZ:
                    destCity = listTimeZones[i - 1]

        # present the results!
        print(userResult.format(userCity))
        userTime.display12()
        print(destResult.format(destCity))
        newTime.display12()
        print(day)

        # figure out the time difference between cities 
        timeDiff = destCity + " is "
        aheadOrBehind = ""

        # hour difference between cities
        if diffHour < 0:
            timeDiff += str((diffHour * -1)) + " hours "
            aheadOrBehind = "behind"
        else:
            timeDiff += str(diffHour) + " hours "
            aheadOrBehind = "ahead of"

        # minute difference, if necessary 
        if diffMinutes > 0:
            timeDiff += "and " + str(diffMinutes) + " minutes "
        elif diffMinutes < 0:
            timeDiff += "and " + str(diffMinutes * -1) + " minutes "

        # finish the sentence and print it
        timeDiff += aheadOrBehind + " " + userCity + "."
        print("\n" + timeDiff)

        # make sure the user's finished
        goAgain = input("\nFinished converting times? (Y/N): ")
        if goAgain.upper() == "Y":
            doLoop = False
        else:
            print("")


"""
Add Time Zone (Option C)

This allows the user to add a time zone to the list of 
available time zones, which is then saved for future use.
"""
def addTimeZone():
    # ask the user for the city and UTC
    newCity = input("Enter a city (City, Nation): ")
    promptUTC = "Enter a UTC for {}: "
    newUTC = input(promptUTC.format(newCity))

    # ensures that the city and UTC have their own lines
    newCity = "\n" + newCity
    newUTC = "\n" + newUTC

    # add the new time zone to the file
    try:
        timeZoneFile = open("timeZones.txt", "a")
        timeZoneFile.write(newCity)
        timeZoneFile.write(newUTC)
        timeZoneFile.close()
    
    # if we can't open the file, handle it
    except:
        print("ERROR: Unable to write to file")


"""
Display Options, "Option ?"

This will display the five ways the user can interact with the 
program.
"""
def displayOptions():
    print("OPTIONS:")
    print("A. Display Time Zones\tB. Convert Times")
    print("C. Add a Time Zone   \t?. Repeat Options")
    print("Q. Quit Program")


"""
Read Time Zones

This will try to read the available time zones from a file into
a list. If it cannot, for whatever reason, it will catch the 
error.
"""
def readTimeZones(listTimeZones):
    # file handled within a "try-except" block for safety
    try:
        timeZoneFile = open("timeZones.txt")

        # read the file into a string
        tempTimeZone = timeZoneFile.read()

        # clear the list to avoid duplication 
        listTimeZones.clear()

        # separate the string into the list
        listTimeZones.extend(tempTimeZone.split("\n"))

        # done with the file, so close it
        timeZoneFile.close()

    # if we can't open the file for some reason...
    except:
        print("ERROR: unable to open file")


"""
Is Valid Time

This will verify that the user's time is valid before sending
the values over to become a Time object.
"""
def isValidTime(hour, min, sec):
    # we're using Earth time, right?
    if hour > 23 or min > 59 or sec > 59:
        return False
    else:
        return True


"""
Is Valid Time Zone

This will verify that the user's choice of time zone is a time
zone within the list
"""
def isValidTimeZone(userUTC, listTimeZones):
    # loop through the whole list
    for i in range(len(listTimeZones)):
        # only focus on the UTCs
        if i % 2 != 0:
            # see if the user's choice is here
            if float(listTimeZones[i]) == userUTC:
                return True
    
    # only runs if the time wasn't found
    return False


"""
Get User Time

This prompts the user for a time and creates a Time object out
of it.
"""
def getUserTime():
    # the user may use their current time or a custom one
    userChoice = input("Use your current time? (Y/N): ")

    # automatically get user's time
    if userChoice.upper() == "Y":
        # leverage the datetime class 
        now = datetime.datetime.now()

        # create a custom Time class from that
        userTime = Time(now.hour, now.minute, now.second)
    
    # let the user manually enter in a time
    else:
        # a word of instruction for the user
        print("\nPlease enter a time in the 24-hour format.\n")

        # loop ensures valid time and the user's choice
        doMainPrompt = True
        while doMainPrompt == True:
            # loops to make sure user's time is valid 
            doSubPrompt = True
            while doSubPrompt == True:
                # prompts 
                userHour = int(input("  Hour:   "))
                userMin  = int(input("  Minute: "))
                userSec  = int(input("  Second: "))

                # if the user input is invalid, the user is reprompted
                if isValidTime(userHour, userMin, userSec):
                    doSubPrompt = False
                else:
                    print("\nPlease enter a valid time.\n")

            # with the valid times, create a Time object
            userTime = Time(userHour, userMin, userSec)

            # display the user's entered time
            print("")
            userTime.display12()
            userTime.display24()

            # ensure this is what the user meant
            goAgain = input("\nIs the above correct? (Y/N): ")
            if goAgain.upper() == "Y":
                doMainPrompt = False
            else:
                doMainPrompt = True
            print("")

    # returns the Time object to be used by other functions
    return userTime


"""
The "Main" Function

All of the parts come together here!
"""
# greets the user
print("\nTIME ZONE CONVERTER\n")
displayOptions()

# sets up a list and a bool for the main loop
listTimeZones = [] 
readTimeZones(listTimeZones)
doMainLoop = True

while doMainLoop == True:
    # Gets user's choice 
    userChoice = input("\n  > ")
    print("")
    
    # Displays the time zones 
    if userChoice.upper() == "A":
        displayTimeZones(listTimeZones)

    # Converts the user's time zone
    elif userChoice.upper() == "B":
        convertTime(listTimeZones)

    # Allows user to add a time zone 
    elif userChoice.upper() == "C":
        addTimeZone()

    # Displays the options again
    elif userChoice.upper() == "?":
        displayOptions()

    # Exits the program 
    elif userChoice.upper() == "Q":
        doMainLoop = False
    
    # Handles unexpected user input 
    else:
        print("Please enter a valid choice.")
