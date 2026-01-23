#import di base
import asyncio,json,tornado,time,random,pymongo,datetime
from pymongo import AsyncMongoClient


#import delle funzione e delle classi
from db import crea_db,crea_partite,inserisci_match

from Publisher import Partita,avvia_partite

from main import HomeHandler,MatchesHandler,WebSocket,main_app,applicazione

#creo database e collection
database, programmati, in_corso, terminati = crea_db()

#creo i Client websocket
websocket_clients = set()

#global partite
partite_programmate = programmati.find().to_list(length=None)

try:
    asyncio.run(applicazione())
    avvia_partite(partite_programmate)
except KeyboardInterrupt:
    print("\nServer spento.")






