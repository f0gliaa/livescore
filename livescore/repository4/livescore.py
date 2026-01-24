#import di base
import asyncio,json,tornado,time,random,pymongo,datetime
from pymongo import AsyncMongoClient


#import delle funzione e delle classi
from db import db

from Publisher import publisher

from main import HomeHandler,MatchesHandler,WebSocket,main_app,applicazione


async def avvia():
    await applicazione() #avvio il server

if __name__=="__main__":
    try:
        asyncio.run(avvia())
    except KeyboardInterrupt:
        print("\nServer spento.")









