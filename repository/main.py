from typing import Union, Optional, Awaitable

import tornado
import tornado.websocket
import asyncio


livescore={}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("client connesso")
    def on_message(self, message):
        print(f"ricevuto: {message}")
        #aggiungi al livescore
    def on_close(self):
        print("client disconnesso")




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

