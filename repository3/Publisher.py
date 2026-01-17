import datetime

import pymongo
import time
import random
import asyncio

from db import database,in_corso,programmati,terminati
from main import websocket_clients

# db
# collections  : "progammate"  "in corso"  "finite"
# { "sport" : "calcio", "squadre" : "k vs z" ,"punti":punti,"ammonizioni":ammonizioni,"interruzioni":interruzioni,"iniziata":True}




async def avvia_partite(partite):
    print("In attesa dell'inizio delle partite...\n")

    while True:
        adesso = datetime.datetime.now()
        tutte_iniziate = False

        for p in partite:  #scorre le partite
            if not p["iniziata"] and adesso >= p["ora_inizio"]:  #se NON è inziata e è arrivato il momento di inizio (di quella partita)
                print(f" Inizia partita tra {p['squadre']} ({p['sport']}) alle {adesso.time()}")
                p["iniziata"] = True  #iniziala
                #sposta la partita e avvia un oggetto Partita
                await in_corso.insert_one(p)
                await programmati.delete_one({"id":p["id"]})  #elimina quella con l'id giusto
                p=Partita(p,websocket_clients)
                await p.start()

        if partite[-1]["iniziata"]:  #se
            tutte_iniziate = True #allora tutte sono iniziate

        if tutte_iniziate:  #se sono tutte iniziate allora FERMA il while
            print("\nTutte le partite sono iniziate.")
            break

        time.sleep(1)  #controlla ogni secondo

#{ "sport" : "calcio", "squadre" : "k vs z" ,"punti":punti,"ammonizioni":ammonizioni,"interruzioni":interruzioni,"iniziata":True}
class Partita:
    def __init__(self, partita,websocket_clients):
        self.id = partita["id"]
        self.sport = partita["sport"]
        self.squadre = partita["squadre"]

        self.punti = 0
        self.ammonizioni = 0
        self.interruzioni = 0

        self.iniziata = True
        #self.finita = False

        self.websocket_clients = websocket_clients

    async def start(self):
        durata = 60  # secondi
        tempo = 0

        print(f"Partita {self.squadre} iniziata")

        while tempo < durata:
            # 50% di probabilità di evento
            if random.randint(0, 1) == 1:
                evento = random.randint(1, 3)

                if evento == 1:
                    self.punti += 1
                    await in_corso.update_one({"id": self.id}, {"$inc": {"punti":1}})
                elif evento == 2:
                    self.ammonizioni += 1
                    await in_corso.update_one({"id": self.id}, {"$inc": {"ammonizioni": 1}})
                elif evento == 3:
                    self.interruzioni += 1
                    await in_corso.update_one({"id": self.id}, {"$inc": {"interruzioni": 1}})
            #
            #invia al client la partita aggiornata ogni secondo
            partita_dict = {
                "id": self.id,
                "squadre": self.squadre,
                "sport": self.sport,
                "punti": self.punti,
                "ammonizioni": self.ammonizioni,
                "interruzioni": self.interruzioni
            }
            for client in self.websocket_clients:
                await client.write_message(partita_dict)


            time.sleep(1)
            tempo += 1

        #PARTITA FINITA
        #self.finita = True

        partita={"id":self.id, "sport" : self.sport, "squadre" : self.squadre ,"punti":self.punti,"ammonizioni":self.ammonizioni,"interruzioni":self.interruzioni,"iniziata":True}
        #sposta la partita da in_corso a terminate
        terminati.insert_one(partita)  #inserisci nei terminati
        in_corso.delete_one({"id":self.id})  #togli dalle in_corso

        print(f"Partita {self.squadre} finita")

async def main():
    partite = await programmati.find().to_list(length=None)
    print(partite)
    await avvia_partite(partite)

asyncio.run(main())

