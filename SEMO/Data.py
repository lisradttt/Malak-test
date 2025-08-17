import asyncio
from pymongo import MongoClient
from pyrogram.client import Client
from pyrogram import filters
from pytgcalls import PyTgCalls
from config import (
    API_ID, API_HASH, MONGO_DB_URI,
    user, dev, call, logger, logger_mode,
    botname, GROUP as GROUPOWNER, CHANNEL as CHANNELOWNER,
    OWNER, OWNER_NAME
)

# ---------------- MongoDB Setup ---------------- #
mo = MongoClient(MONGO_DB_URI)
moo = mo["data"]

# جداول MongoDB
db = moo  # لتسهيل الاستيراد في SEMO.py كـ semo_db
Bots = moo.alli
bot_name_db = moo.bot_name
channeldb = moo.ch
groupdb = moo.gr
channeldbsr = moo.chsr
groupdbsr = moo.grsr
mustdb = moo.must

# ---------------- In-memory caches ---------------- #
CHANNEL = {}
GROUP = {}
CHANNELsr = {}
GROUPsr = {}
devname = {}
boot = {}
must = {}

# ---------------- Helper: get_data ---------------- #
def get_data(collection_name: str, query: dict):
    """Generic function to get data from a collection"""
    col = getattr(moo, collection_name, None)
    if not col:
        return None
    return col.find_one(query)

# ---------------- Developer ---------------- #
async def get_dev(bot_username: str):
    devv = dev.get(bot_username)
    if not devv:
        bot = Bots.find_one({"bot_username": bot_username})
        if bot:
            devv = bot.get("dev")
            dev[bot_username] = devv
            return devv
    return devv

async def get_dev_name(client: Client, bot_username: str):
    name = devname.get(bot_username)
    if not name:
        bot = Bots.find_one({"bot_username": bot_username})
        if bot:
            dev_id = bot.get("dev")
            if dev_id:
                chat = await client.get_chat(dev_id)
                dev_first_name = getattr(chat, "first_name", "Unknown")
                devname[bot_username] = dev_first_name
                return dev_first_name
    return name
# ---------------- Bot Name ---------------- #
async def get_bot_name(bot_username: str):
    name = botname.get(bot_username)
    if not name:
        bot = bot_name_db.find_one({"bot_username": bot_username})
        if bot:
            botname[bot_username] = bot.get("bot_name", "نونا")
            return botname[bot_username]
        return "نونا"
    return name

async def set_bot_name(bot_username: str, BOT_NAME: str):
    botname[bot_username] = BOT_NAME
    bot_name_db.update_one(
        {"bot_username": bot_username},
        {"$set": {"bot_name": BOT_NAME}},
        upsert=True
    )

# ---------------- Bot Group & Channel ---------------- #
async def get_group(bot_username: str):
    name = GROUP.get(bot_username)
    if not name:
        bot = groupdb.find_one({"bot_username": bot_username})
        if bot:
            GROUP[bot_username] = bot.get("group", GROUPOWNER)
            return GROUP[bot_username]
        return GROUPOWNER
    return name

async def set_group(bot_username: str, group: str):
    GROUP[bot_username] = group
    groupdb.update_one(
        {"bot_username": bot_username},
        {"$set": {"group": group}},
        upsert=True
    )

async def get_channel(bot_username: str):
    name = CHANNEL.get(bot_username)
    if not name:
        bot = channeldb.find_one({"bot_username": bot_username})
        if bot:
            CHANNEL[bot_username] = bot.get("channel", CHANNELOWNER)
            return CHANNEL[bot_username]
        return CHANNELOWNER
    return name

async def set_channel(bot_username: str, channel: str):
    CHANNEL[bot_username] = channel
    channeldb.update_one(
        {"bot_username": bot_username},
        {"$set": {"channel": channel}},
        upsert=True
    )

# ---------------- SR Group & Channel ---------------- #
async def get_groupsr(bot_username: str):
    name = GROUPsr.get(bot_username)
    if not name:
        bot = groupdbsr.find_one({"bot_username": bot_username})
        if bot:
            GROUPsr[bot_username] = bot.get("groupsr", GROUPOWNER)
            return GROUPsr[bot_username]
        return GROUPOWNER
    return name

async def set_groupsr(bot_username: str, groupsr: str):
    GROUPsr[bot_username] = groupsr
    groupdbsr.update_one(
        {"bot_username": bot_username},
        {"$set": {"groupsr": groupsr}},
        upsert=True
    )

async def get_channelsr(bot_username: str):
    name = CHANNELsr.get(bot_username)
    if not name:
        bot = channeldbsr.find_one({"bot_username": bot_username})
        if bot:
            CHANNELsr[bot_username] = bot.get("channelsr", CHANNELOWNER)
            return CHANNELsr[bot_username]
        return CHANNELOWNER
    return name

async def set_channelsr(bot_username: str, channelsr: str):
    CHANNELsr[bot_username] = channelsr
    channeldbsr.update_one(
        {"bot_username": bot_username},
        {"$set": {"channelsr": channelsr}},
        upsert=True
    )

# ---------------- Must Join ---------------- #
async def must_join(bot_username: str):
    status = must.get(bot_username)
    if not status:
        bot = mustdb.find_one({"bot_username": bot_username})
        if bot:
            must[bot_username] = bot.get("getmust", "معطل")
            return must[bot_username]
        return "معطل"
    return status

async def set_must(bot_username: str, m: str):
    status = "معطل" if m == "• تعطيل الاشتراك الإجباري •" else "مفعل"
    must[bot_username] = status
    mustdb.update_one(
        {"bot_username": bot_username},
        {"$set": {"getmust": status}},
        upsert=True
    )

# ---------------- Userbot, Call, App & Logger ---------------- #
async def get_userbot(bot_username: str):
    userbot = user.get(bot_username)
    if not userbot:
        bot = Bots.find_one({"bot_username": bot_username})
        if bot:
            session = bot.get("session")
            userbot = Client("SEMO", api_id=API_ID, api_hash=API_HASH, session_string=session)
            user[bot_username] = userbot
            return userbot
    return userbot

async def get_call(bot_username: str):
    call_client = call.get(bot_username)
    if not call_client:
        userbot = await get_userbot(bot_username)
        call_client = PyTgCalls(userbot, cache_duration=100)
        await call_client.start()
        call[bot_username] = call_client
        return call_client
    return call_client

async def get_app(bot_username: str):
    app_client = boot.get(bot_username)
    if not app_client:
        bot = Bots.find_one({"bot_username": bot_username})
        if bot:
            token = bot.get("token")
            app_client = Client(
                "SEMO",
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=token,
                plugins=dict(root="SEMO")
            )
            boot[bot_username] = app_client
            return app_client
    return app_client

async def get_logger(bot_username: str):
    loggero = logger.get(bot_username)
    if not loggero:
        bot = Bots.find_one({"bot_username": bot_username})
        if bot:
            loggero = bot.get("logger")
            logger[bot_username] = loggero
            return loggero
    return loggero

async def get_logger_mode(bot_username: str):
    log_mode = logger_mode.get(bot_username)
    if not log_mode:
        bot = Bots.find_one({"bot_username": bot_username})
        if bot:
            log_mode = bot.get("logger_mode")
            logger_mode[bot_username] = log_mode
            return log_mode
    return log_mode

# ---------------- Ready ---------------- #
if __name__ == "__main__":
    print("SEMO Bot Module Loaded Successfully")
