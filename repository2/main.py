from typing import Union, Optional, Awaitable

import tornado
import tornado.websocket
import asyncio
import json
from db import database,in_corso,programmati,terminati
livescore={}

websocket_clients = set()  #set dei websocket messo globale

class MatchesHandler(tornado.web.RequestHandler):
    async def get(self):
        partite_live = await in_corso.find().to_list(length=100)
        partite_prog = await programmati.find().to_list(length=100)
        partite_fin = await terminati.find().to_list(length=100)

        partite=[partite_prog,partite_live,partite_fin]
        self.set_header("Content-Type", "application/json")
        await self.render("home.html", partite=partite)

class LiveScoreSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Nuovo client WebSocket connesso")
        websocket_clients.add(self)

    def on_close(self):
        websocket_clients.remove(self)
        print("Client WebSocket disconnesso")

    async def send_update(self, partita):
        """Invia aggiornamento a tutti i client connessi"""
        msg = json.dumps(partita)
        for client in websocket_clients:
            try:
                await client.write_message(msg)
            except:
                pass  # ignora errori se il client è già chiuso





def make_app():
    return tornado.web.Application(
        [
            (r"/livescore", MainHandler),
        ],
        autoreload=True,
        debug=True
    )




async def main():
    app = make_app()
    app.listen(2000)
    print(f"Server avviato su http://localhost:2000")
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer spento.")

