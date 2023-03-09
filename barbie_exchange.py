# Fonction d'échange avec barbie
import re
import csv

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer


PATH = "training_data/transcript/"
FILE_NAMES = ["diamond_castle", "fairytopia", "princess_pauper", "twelve_princess", "video_game"]

MAX_SAMPLES = 5_000_000

def preprocess_sentence(sentence):
    sentence = sentence.lower().strip()
    # creating a space between a word and the punctuation following it
    # eg: "he is a boy." => "he is a boy ."
    sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
    # Get rid of unnecessary space
    sentecne = re.sub(r'[" "]+', " ", sentence)
    # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
    sentence = re.sub(r"[^a-zA-Z?.,!]+", " ", sentence)
    sentence = sentence.strip()
    # adding a start and an end token to the sentence
    return sentence

def load_conversations():
    # dictionary of line id to text
    id2line = {}
    with open('training_data/movie_lines.txt', encoding = 'latin-1', errors = 'ignore') as file:
        lines = file.readlines()
    for line in lines:
        parts = line.replace('\n', '').split(' +++$+++ ')
        id2line[parts[0]] = parts[4]
        
    inputs, outputs = [], []
    with open('training_data/movie_conversations.txt', 
                     encoding = 'latin-1', errors = 'ignore') as file:
        lines = file.readlines()
    for line in lines:
        parts = line.replace('\n', '').split(' +++$+++ ')
        # get conversation in a list of line ID
        conversation = [line[1:-1] for line in parts[3][1:-1].split(', ')]
        for i in range(len(conversation) - 1):
            inputs.append(preprocess_sentence(id2line[conversation[i]]))
            outputs.append(preprocess_sentence(id2line[conversation[i + 1]]))
            if len(inputs) >= MAX_SAMPLES:
                return inputs, outputs
    return inputs, outputs

def fine_tune_convos():
    """Fine tune the chatbot with the data of Cornell Movie-Dialogs Corpus"""
    chatbot = ChatBot('Test Convos')
    trainer = ListTrainer(chatbot)

    questions, answers = load_conversations()
    resultat = list(zip(questions, answers))

    for i in range(len(resultat)):
        trainer.train(resultat[i])
    
    return chatbot

def train_barbie_bot():
    """Train the chatbot with the data in the chatterbot corpus"""
    chatbot = ChatBot('Barbie')

    trainer = ChatterBotCorpusTrainer(chatbot)
    # Train on english corpus
    trainer.train(
        "chatterbot.corpus.english",
    )
    return chatbot

def fine_tune_barbie():
    """Fine tune the chatbot with the data in the csv files that match the script of barbie movies"""
    chatbot = ChatBot('Test Bot')
    trainer = ListTrainer(chatbot)

    for file_name in FILE_NAMES:
        with open(f'{PATH}{file_name}.csv') as csvfile:
            rows = csv.reader(csvfile)
            res = list(zip(*rows))

        for i in range(len(res)):
            trainer.train(res[i])
           
    return chatbot

def call_barbie(training=False):
    """Call the chatbot and train it if training is True"""
    chatbot = ChatBot('Test test',
                    #storage_adapter='chatterbot.storage.SQLStorageAdapter',
                    #database_uri='jdbc:sqlite:/Users/kenza/PycharmProjects/pythonProject/db.sqlite3'
                      )
    
    if training:
        #train_barbie_bot()
        #fine_tune_barbie()
        fine_tune_convos()

    return chatbot



"""
chatbot = call_barbie()

while True:
    try:
        bot_input = chatbot.get_response(input())
        print(bot_input)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break

response = chatbot.get_response('Who are you?')
print(response)

"""

#/usr/local/Cellar/portaudio/19.7.0