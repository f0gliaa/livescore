from bson import ObjectId


class DatabaseInterface:
    def __init__(self, db):
        self._users = db["users"]
        self._tasks = db["tasks"]

    # ---------- USERS ----------

    async def get_user_by_email(self, email: str):
        return await self._users.find_one({"email": email})

    async def create_user(self, email: str, hashed_password: bytes):
        return await self._users.insert_one({
            "email": email,
            "password": hashed_password
        })

    # TASKS

    async def get_tasks_by_user(self, user_id: str):
        cursor = self._tasks.find({"user_id": ObjectId(user_id)})
        return [t async for t in cursor]

    async def create_task(self, user_id: str, text: str):
        return await self._tasks.insert_one({
            "user_id": ObjectId(user_id),
            "text": text,
            "done": False
        })

    async def update_task_done(self, task_id: str, user_id: str, done: bool):
        return await self._tasks.update_one(
            {
                "_id": ObjectId(task_id),
                "user_id": ObjectId(user_id)
            },
            {"$set": {"done": bool(done)}}
        )

    async def delete_task(self, task_id: str, user_id: str):
        return await self._tasks.delete_one({
            "_id": ObjectId(task_id),
            "user_id": ObjectId(user_id)
        })

