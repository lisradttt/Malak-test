import os
import asyncio
from pyrogram.client import Client
from pytgcalls import PyTgCalls, idle
from pyromod import listen  # لو عندك Plugins أو تريد التفاعل مع Pyromod
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_

from config import API_ID, API_HASH, BOT_TOKEN, MONGO_DB_URI
from bot import sync_time, start_bot  # تأكد أن الدالتين موجودين في bot.py

# ---------------- MongoDB Setup ---------------- #
mongo_client = _mongo_client_(MONGO_DB_URI)
db = mongo_client["data"]  # مهم يكون نفس الاسم المستخدم في SEMO.py
# الآن db متوافق مع SEMO.py وكافة الجداول داخلها

# ---------------- Main Function ---------------- #
async def main():
    # مزامنة الوقت لتجنب أي مشاكل في البوت
    sync_time()
    
    # بدء تشغيل البوت
    await start_bot()
    print("[INFO]: تم تشغيل البوت بنجاح.")
    
    # الانتظار حتى يتم إيقاف البوت
    await idle()

# ---------------- Entry Point ---------------- #
if __name__ == "__main__":
    # تشغيل asyncio
    asyncio.run(main())
