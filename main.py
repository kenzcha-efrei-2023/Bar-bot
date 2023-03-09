from audio_file_management import record_to_file
from alerte import takeCommand, alert, barbie_speak
from wit import Wit
from barbie_exchange import call_barbie
access_token = "SSSEKEYWIIPOCH2YITSUMWJVUGGP5ORS"

client = Wit(access_token)

#nlp_data = client.message('Is it okay if we take some time to stretch and warm up first')
while True :
    try:
        while not alert() :
            pass
        barbie_speak("yes ?")
        nlp_data = client.message(takeCommand())
        print(nlp_data)
        intent = nlp_data["intents"][0]["name"]
        if intent == "metronome":
            print("Metronome")
            print(nlp_data["entities"]["beats:beats"][0]["body"], nlp_data["entities"]["tempo:tempo"][0]["body"])
            barbie_speak("Changing metronome")
        elif intent == "next_page":
            print("next_page")
            barbie_speak("Next page")
        elif intent == "previous_page":
            print("previous_page")
            barbie_speak("Previous page")
        elif intent == "backing_track":
            print("backing_track")
        elif intent == "play" :
            barbie_speak("Starting metronome")
            print("play")
        elif intent == "stop":
            barbie_speak("Stopping metronome")
            print("stop")
        elif intent == "change_partition":
            barbie_speak("Changing the sheet music")
            print("change_partition")
            print(nlp_data["entities"]["title:title"][0]["body"])
        elif intent == "pause":
            barbie_speak("Time for the break ! Let's have a chat.")
            print("pause")
            barbie = call_barbie()
            while True :
                answer = takeCommand()
                if answer.lower() == "bye":
                    barbie_speak("Let's resume the practice")
                    break
                else :
                    rep = barbie.get_response(answer)
                    barbie_speak(rep)
        elif intent == "register":
            barbie_speak("Recording now in 3 ... 2 ... 1 ...")
            record_to_file('output.wav')
    except Exception as e:
        barbie_speak("I didn't get it")
        pass
''''''
"""

if __name__ == '__main__':    
    while True:
        if alert():
            if takeCommand().lower() == "au revoir":
                print("A la revoyure")

"""
"""
print('#' * 80)
print("Please speak word(s) into the microphone")
print('Press Ctrl+C to stop the recording')

record_to_file('output.wav')

print("Result written to output.wav")
print('#' * 80)
"""
