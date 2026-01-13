from pymongo import AsyncMongoClient


MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "db_score"

client = AsyncMongoClient(MONGO_URL)  # creo il client
database = client[DB_NAME]  # creo database collegato al client

# creazione collections
programmati = database["programmati"]
in_corso = database["in_corso"]
terminati = database["terminati"]

#PARTE DI CREARE DEI MATCH

import datetime
import random as rnd

squadre=["modena","roma","milano","cesena","torino","empoli","bologna","napoli","palermo","inter"]
sport=["calcio","tennis","basket","volano","lotta-greco-romana"]

def crea_partite():
    lista=[]
    for i in range(5):

        prima_squadra=rnd.choice(squadre)
        seconda_squadra=rnd.choice(squadre)

        while not prima_squadra == seconda_squadra:
            seconda_squadra=rnd.choice(squadre)

        p={"ora_inizio": datetime.timedelta(seconds=rnd.randint(10,60)),"sport" : rnd.choice(sport), "squadre" : f"{prima_squadra} vs {seconda_squadra}" ,"punti":0,"ammonizioni":0,"interruzioni":0}
        lista.append(p)
    return lista

#partite da mettere nei progammati
#p1={"ora_inizio": 5,"sport" : "calcio", "squadre" : "k vs z" ,"punti":0,"ammonizioni":0,"interruzioni":0}


# await collection.insert_one({"nome": "Mario", "citta": "Roma"})

lista_match=crea_partite()

async def inserisci_match(lista_match):
    for p in lista_match:
        await programmati.insert_one(p)

if __name__=="__main__":
    print(lista_match)
    inserisci_match(lista_match)

