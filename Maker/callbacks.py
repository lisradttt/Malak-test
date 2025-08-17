# ---------------- Python ----------------
import asyncio

# ---------------- Pyrogram ----------------
from pyrogram.client import Client as PyroClient  # استدعاء Client من pyrogram.client لتجنب التحذيرات
from pyrogram.enums import ParseMode

# ---------------- Telethon ----------------
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon import Button

# ---------------- Config ----------------
import config

# هنا سؤال المستخدمين عن البيانات
async def ask_ques(bot, event, ques, is_pass=False):
    await event.respond(ques)
    response = await bot.wait_event(
        event.my_class(chat_id=event.chat_id)  # استبدل 'class' بـ 'my_class'
    )
    if is_pass:
        return response.message.message
    return response.message.message.strip()

# هنا الأزرار
def buttons_ques():
    return [
        [Button.inline("📱 توليد تيرمكس (Telethon)", data=b"t"),
         Button.inline("🤖 توليد بايروجرام (Pyrogram)", data=b"p")]
    ]

# التوليد
async def generate_session(bot, event, telethon=True):
    try:
        if telethon:
            await event.respond("🔄 جاري توليد سيشن Telethon ...")
            async with TelegramClient(StringSession(), config.API_ID, config.API_HASH) as client:
                string = client.session.save()
                await event.respond(f"✅ تم توليد سيشن Telethon:\n\n`{string}`")
        else:
            await event.respond("🔄 جاري توليد سيشن Pyrogram ...")
            async with PyroClient(
                "my_account",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                in_memory=True
            ) as app:
                string = await app.export_session_string()
                await event.respond(f"✅ تم توليد سيشن Pyrogram:\n\n`{string}`")
    except Exception as e:
        await event.respond(f"❌ حصل خطأ:\n`{str(e)}`")
