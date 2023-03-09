import mac_say
from audio_file_management import takeCommand

barbie = mac_say


def barbie_speak(content):
    """Speech function"""
    barbie.say([content, "-v","Karen"])
    print(content)


def alert():
    """Alert function to start Barbie
    Still in progress"""

    if takeCommand().lower() == "barbie":
        print("Je vous écoute")
        return True
    else:
        return False
