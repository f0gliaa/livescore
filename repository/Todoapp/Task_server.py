import asyncio
import tornado.web

from backend.db.db import COOKIE_SECRET, PORT
from backend.handlers.auth import RegisterHandler, LoginHandler, LogoutHandler
from backend.handlers.tasks import TasksHandler, TaskUpdateHandler, TaskDeleteHandler


def make_app():
    return tornado.web.Application(
        [
            (r"/api/register", RegisterHandler),
            (r"/api/login", LoginHandler),
            (r"/api/logout", LogoutHandler),

            (r"/api/tasks", TasksHandler),
            (r"/api/tasks/([a-f0-9]{24})", TaskUpdateHandler),
            (r"/api/tasks/([a-f0-9]{24})/delete", TaskDeleteHandler),

            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
            (r"/", tornado.web.RedirectHandler, {"url": "/static/login.html"}),
        ],
        cookie_secret=COOKIE_SECRET,
        autoreload=True,
        debug=True
    )


async def main():
    app = make_app()
    app.listen(PORT)
    print(f"Server avviato su http://localhost:{PORT}")
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer spento.")

