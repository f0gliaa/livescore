from pymongo import AsyncMongoClient

#PARTE DI CREARE DEI MATCH
import asyncio
import datetime
import random
import os




async def crea_db():
    host= os.getenv("MONGO_HOST", "localhost")
    MONGO_URL = f"mongodb://{host}:27017"
    DB_NAME = "db_score"

    client = AsyncMongoClient(MONGO_URL)  # creo il client
    database = client[DB_NAME]  # creo database collegato al client

    # creazione collections
    programmati = database["programmati"]
    in_corso = database["in_corso"]
    terminati = database["terminati"]

    #svuota collezioni
    await programmati.delete_many({})
    await in_corso.delete_many({})
    await terminati.delete_many({})

    return programmati, in_corso, terminati

def crea_partite():
    squadre = ["modena","roma","milano","cesena","torino","empoli","bologna","napoli","palermo","inter"]
    sport = ["calcio","tennis","basket","volano","lotta-greco-romana"]

    partite = []
    ora_base = datetime.datetime.now()  #prende il tempo da adesso

    id=0
    for i in range(5):
        s1, s2 = random.sample(squadre, 2)   #prendo due squadre a caso dalla lista

        partita = {
            "id": id,
            "ora_inizio": str(ora_base + datetime.timedelta(seconds=20 * i)), #ogni partita inizia ogni 20 secondi
            "sport": random.choice(sport),
            "squadre": f"{s1} vs {s2}",
            "punti": 0,
            "ammonizioni": 0,
            "interruzioni": 0,
        }

        partite.append(partita)
        id+=1

    return partite  #programmate

#partite da mettere nei progammati
#p1={"ora_inizio": 5,"sport" : "calcio", "squadre" : "k vs z" ,"punti":0,"ammonizioni":0,"interruzioni":0}



# await collection.insert_one({"nome": "Mario", "citta": "Roma"})



async def inserisci_match(lista_match,programmati):    #inserisco i match nella collection "programmati"
    for p in lista_match:
        await programmati.insert_one(p)

""" 
async def main():
    lista_match = crea_partite()
    print(lista_match)
    await inserisci_match(lista_match,programmati)
"""


async def db():
    database, programmati, in_corso, terminati = crea_db()
    partite_programmate=crea_partite()
    await inserisci_match(partite_programmate,programmati)
    return programmati, in_corso, terminati





