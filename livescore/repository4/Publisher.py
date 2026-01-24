import datetime

import pymongo
import time
import random
import asyncio

from db import crea_db,crea_partite,inserisci_match,db
from main import websocket_clients
from main import websocket_clients
import json
# db
# collections  : "progammate"  "in corso"  "finite"
# { "sport" : "calcio", "squadre" : "k vs z" ,"punti":punti,"ammonizioni":ammonizioni,"interruzioni":interruzioni,"iniziata":True}




async def avvia_partite(partite_programmate):
    print("In attesa dell'inizio delle partite...\n")

    while True:
        adesso = datetime.datetime.now()
        tutte_iniziate = False

        for p in partite_programmate:  #scorre le partite
            if adesso >= p["ora_inizio"]:  #se è arrivato il momento di inizio (di quella partita)
                print(f" Inizia partita tra {p['squadre']} ({p['sport']}) alle {adesso.time()}")
                #sposta la partita e avvia un oggetto Partita
                await in_corso.insert_one(p)
                await programmati.delete_one({"id":p["id"]})  #elimina quella con l'id giusto
                p=Partita(p)
                await p.start()

        if programmati.count_documents({})==0:  #se la collection programmati è vuota
            tutte_iniziate = True #allora tutte sono iniziate

        if tutte_iniziate:  #se sono tutte iniziate allora FERMA il while
            print("\nTutte le partite sono iniziate.")
            break

        time.sleep(1)  #controlla ogni secondo



#{ "sport" : "calcio", "squadre" : "k vs z" ,"punti":punti,"ammonizioni":ammonizioni,"interruzioni":interruzioni,"iniziata":True}
class Partita:
    partite=[programmati,in_corso,terminati]  # ogni volta devo mandare questo in websocket db() mi passa le partite [programmati,in_corso,terminati]
    def __init__(self, partita):
        self.id = partita["id"]
        self.sport = partita["sport"]
        self.squadre = partita["squadre"]

        self.punti = 0
        self.ammonizioni = 0
        self.interruzioni = 0


        self.partita=partita
        self.__class__.partite[1].append(self.partita) #la appende a quelle in corso
        self.__class__.partite[0].delete(self.partita)  #cancella la partita che ha messo in in-corso

        #self.websocket_clients = websocket_clients  #CLIENT A CUI INVIARE I DATI

    def send_partite(self):  #   INVIO DELLE PARTITE
        for ws_c in websocket_clients:
            ws_c.write_message(json.dumps(self.__class__.partite))

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
                    await in_corso.update_one({"id": self.id}, {"$inc": {"punti":1}})  #modifiche al database
                elif evento == 2:
                    self.ammonizioni += 1
                    await in_corso.update_one({"id": self.id}, {"$inc": {"ammonizioni": 1}})
                elif evento == 3:
                    self.interruzioni += 1
                    await in_corso.update_one({"id": self.id}, {"$inc": {"interruzioni": 1}})
            #
            #invia al client le partite
            self.send_partite()  #manda partite (ogni secondo)

            time.sleep(1)
            tempo += 1

        #PARTITA FINITA
        #self.finita = True
        self.__class__.partite[1].delete(self.partita)  #toglila dalle in_corso
        self.__class__.partite[2].append(self.partita)  #appendila alle terminate
        self.send_partite()  # manda partite (una volta)

        partita={"id":self.id, "sport" : self.sport, "squadre" : self.squadre ,"punti":self.punti,"ammonizioni":self.ammonizioni,"interruzioni":self.interruzioni,"iniziata":True}
        #sposta la partita da in_corso a terminate
        terminati.insert_one(partita)  #inserisci nei terminati
        in_corso.delete_one({"id":self.id})  #togli dalle in_corso

        print(f"Partita {self.squadre} finita")

async def publisher():
    global programmati, in_corso, terminati
    programmati, in_corso, terminati = await db()
    partite_programmate = await programmati.find()
    await avvia_partite(partite_programmate)
    return programmati, in_corso, terminati

"""
if __name__=="__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer spento.")
"""
