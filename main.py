import os
from fastapi import FastAPI, Header, HTTPException
from telethon import TelegramClient

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
RESOLVER_KEY = os.environ["RESOLVER_KEY"]

app = FastAPI()

client = TelegramClient(
    "korsan_resolver",
    API_ID,
    API_HASH
)


@app.on_event("startup")
async def startup():
    await client.start(bot_token=BOT_TOKEN)


@app.on_event("shutdown")
async def shutdown():
    await client.disconnect()


@app.get("/")
async def home():
    return {
        "status": "online",
        "service": "KORSAN USER RESOLVER"
    }


@app.get("/resolve")
async def resolve(
    username: str,
    x_resolver_key: str = Header(default="")
):

    if x_resolver_key != RESOLVER_KEY:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized"
        )

    username = username.strip().lstrip("@")

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username gerekli"
        )

    try:
        entity = await client.get_entity(username)

        return {
            "ok": True,
            "id": entity.id,
            "username": getattr(entity, "username", username),
            "first_name": getattr(entity, "first_name", ""),
            "last_name": getattr(entity, "last_name", "")
        }

    except Exception as e:

        return {
            "ok": False,
            "error": str(e)
        }
