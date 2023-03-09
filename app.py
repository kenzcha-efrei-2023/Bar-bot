from audio_file_management import record_to_file, whisper_listen
from alerte import takeCommand, alert, barbie_speak
from wit import Wit
from barbie_exchange import call_barbie
from flask import Flask
from flask_socketio import SocketIO
import time
from random import choice
from datetime import datetime
import difflib
import json
access_token = "SSSEKEYWIIPOCH2YITSUMWJVUGGP5ORS"

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, cors_allowed_origins="http://localhost:8080")
thread = None
client = Wit(access_token)
FILE = "partition/description.json"

def get_name(title_search):
    with open(FILE, 'r') as f:
        data = json.load(f)
    ma = None
    max_sim = 0
    for key, value in data.items():
        similarite = difflib.SequenceMatcher(None, value['title'], title_search).ratio()
        if similarite > max_sim:
            ma = value['id']
            max_sim = similarite
    return ma

"""
boucle de l'appli
"""
def appli_test():

    while True :
        try:
            while not alert() :
                pass
            socketio.emit("start_talking", {"content": ""})
            socketio.emit("message",  {"content":"Yes ?"})
            barbie_speak("yes ?")
            socketio.emit("stop_talking", {"content": ""})
            nlp_data = client.message(takeCommand())
            print(nlp_data)
            intent = nlp_data["intents"][0]["name"]
            if intent == "metronome":
                print("Metronome")
                values = [int(nlp_data["entities"]["beats:beats"][0]["body"]), int(nlp_data["entities"]["tempo:tempo"][0]["body"])]
                socketio.emit("metronome",  {"state": 0,"tempo":max(values), "mesure":min(values), "change_state":False})
                socketio.emit("message",  {"content":"Changing metronome"})
                socketio.emit("start_talking", {"content": ""})
                barbie_speak("Changing metronome")
                socketio.emit("stop_talking", {"content": ""})

            elif intent == "next_page":
                socketio.emit("partition", {"next_page" : True, "prev_page": False,"change_part":False,"page" : 5 , "change_page":False, "id_part":0})
                socketio.emit("message",  {"content":"Next page"})
                socketio.emit("start_talking", {"content": ""})
                barbie_speak("Next page")
                socketio.emit("stop_talking", {"content": ""})
            elif intent == "previous_page":
                socketio.emit("partition", {"next_page" : False, "prev_page": True,"change_part":False,"page" : 5 , "change_page":False, "id_part":0})
                socketio.emit("message",  {"content":"Previous page"})
                socketio.emit("start_talking", {"content": ""})
                barbie_speak("Previous page")
                socketio.emit("stop_talking", {"content": ""})
            elif intent == "backing_track":
                print("backing_track")
            elif intent == "play" :
                socketio.emit("metronome",  {"state": 1,"tempo":100, "mesure":4, "change_state":True})
                socketio.emit("message",  {"content":"Starting metronome"})
                socketio.emit("start_talking", {"content": ""})
                barbie_speak("Starting metronome")
                socketio.emit("stop_talking", {"content": ""})
            elif intent == "stop":
                socketio.emit("metronome",  {"state": 0,"tempo":100, "mesure":4, "change_state":True})
                socketio.emit("message",  {"content":"Stopping metronome"})
                socketio.emit("start_talking", {"content": ""})
                barbie_speak("Stopping metronome")
                socketio.emit("stop_talking", {"content": ""})
                print("stop")
            elif intent == "change_partition":
                socketio.emit("message",  {"content":"Changing the sheet music"})
                socketio.emit("start_talking", {"content": ""})
                barbie_speak("Changing the sheet music")
                socketio.emit("stop_talking", {"content": ""})
                print("name : "+nlp_data["entities"]["title:title"][0]["body"])
                print("id : " + str(get_name(nlp_data["entities"]["title:title"][0]["body"])))
                socketio.emit("partition", {"next_page" : False, "prev_page": False,"change_part":True,"page" : 1, "change_page":False , "id_part":get_name(nlp_data["entities"]["title:title"][0]["body"])})
            elif intent == "pause":
                socketio.emit("start_talking", {"content": ""})
                socketio.emit("message",  {"content":"Time for the break ! Let's have a chat."})
                barbie_speak("Time for the break ! Let's have a chat.")
                socketio.emit("stop_talking", {"content": ""})
                print("pause")
                barbie = call_barbie()
                while True :
                    answer = takeCommand()
                    if answer.lower() == "bye":
                        socketio.emit("start_talking", {"content": ""})
                        socketio.emit("message",  {"content":"Let's resume the practice"})
                        barbie_speak("Let's resume the practice")
                        socketio.emit("stop_talking", {"content": ""})
                        break
                    else :
                        rep = barbie.get_response(answer)
                        socketio.emit("message",  {"content":str(rep)})
                        socketio.emit("start_talking", {"content": ""})
                        barbie_speak(str(rep))
                        socketio.emit("stop_talking", {"content": ""})
            elif intent == "register":
                socketio.emit("message",  {"content":"Recording 30 seconds now in 3 ... 2 ... 1 ..."})
                socketio.emit("start_talking", {"content": ""})
                barbie_speak("Recording 30 seconds now in 3 ... 2 ... 1 ...")
                socketio.emit("stop_talking", {"content": ""})
                now = datetime.now()
                record_to_file("record_"+now.strftime("%m%d%Y%H%M%S")+".wav")
                socketio.emit("message",  {"content":"Done recording"})
                socketio.emit("start_talking", {"content": ""})
                barbie_speak("Done recording")
                socketio.emit("stop_talking", {"content": ""})
        except Exception as e:
            print(e)
            socketio.emit("message",  {"content":"I didn't get it"})
            socketio.emit("start_talking", {"content": ""})
            barbie_speak("I didn't get it")
            socketio.emit("stop_talking", {"content": ""})
            pass

@socketio.on('connect')
def client_connect():
    global thread
    if thread is None :
        thread = socketio.start_background_task(target=appli_test)
    print("Client connected to server !")
    pass


@socketio.on('disconnect')
def client_connect():
    print("Client disconnected to server.")


if __name__ == '__main__' :
    app.debug = True
    socketio.run(app, port=2346)





