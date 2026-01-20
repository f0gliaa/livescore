from typing import Union, Optional, Awaitable

import tornado
import tornado.websocket
import asyncio
import json
from db import database,in_corso,programmati,terminati
livescore={}

websocket_clients = set()  #set dei websocket messo globale


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")

class MatchesHandler(tornado.web.RequestHandler):

    async def get(self):
        partite_prog = await programmati.find().to_list(100)
        partite_live = await in_corso.find().to_list(100)
        partite_fin = await terminati.find().to_list(100)

        def serialize(p):
            p["_id"] = str(p["_id"])
            if "ora_inizio" in p:
                p["ora_inizio"] = p["ora_inizio"].isoformat()  # datetime -> string
            return p

        self.write({
            "programmati": [serialize(p) for p in partite_prog],
            "live": [serialize(p) for p in partite_live],
            "terminati": [serialize(p) for p in partite_fin]
        })

class WebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Nuovo client WebSocket connesso")
        websocket_clients.add(self)

    def on_close(self):
        websocket_clients.remove(self)
        print("Client WebSocket disconnesso")

    async def send_update(self, partita):
        #invio degli aggiornamenti
        msg = json.dumps(partita)
        for client in websocket_clients:
            try:
                await client.write_message(msg)
            except: #se client è gia chiuso
                pass





def make_app():
    return tornado.web.Application(
        [
            (r"/", MatchesHandler),
            (r"/matches", MatchesHandler),
            (r"/ws", WebSocket),
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

