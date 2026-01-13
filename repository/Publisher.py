import datetime

import pymongo
import time
import random

# codice per creare/accedere al database
from pymongo import AsyncMongoClient

from db import database,in_corso,programmati,terminati


# db
# collections  : "progammate"  "in corso"  "finite"
# { "sport" : "calcio", "squadre" : "k vs z" ,"punti":punti,"ammonizioni":ammonizioni,"interruzioni":interruzioni}
t=0

def tempo():
    s=0
    m=0
    while True:
        s +=1
        if s>=60:
            s=0
            m+=1
        return f"{m} : {s}"




lista_programmati = []


class Sposta_Match():
    def __init__(self):
        self.db = database

    def run(self):
        while True:
            for partita in lista_programmati:
                if partita["ora inizo"] == datetime.datetime.now():
                    partita.start()


class Partita():
    id = 0

    def __init__(self, sport, squadre):
        self.sport = sport
        self.squadre = squadre
        self.id = self.__class__.id

    def start(self):
        tempo = 0
        punti = 0
        ammonizioni = 0
        interruzioni = 0
        #
        partita = {"id": self.id, "sport": self.sport, "punti": punti, "ammonizioni": ammonizioni,
                   "interruzioni": interruzioni}

        while tempo < 60:

            if not xxx:
                continue

            # azioni
            scelta = random.randint(0, 1)  # scelta se aumentare qualcosa o no
            if scelta == 1:  # se viene aumentato qualcosa
                r = random.randint(1, 3)  # quale valore scegliere da aumentare
                if r == 1:
                    partita["punti"] += 1
                if r == 2:
                    partita["ammonizioni"] += 1
                if r == 3:
                    partita["interruzioni"] += 1

            await in_corso.update_one({"id": self.id}, )
            # aumenta tempo
            time.sleep(1)  # aspetta un secondo
            tempo += 1


partita = Partita()
lista_programmati.append(partita)

ora_inizio = d1 + datetime.timedelta(days=rnd.randint(1, 4))
