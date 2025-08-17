import asyncio
import platform
import subprocess
from pyrogram.client import Client
from pyrogram.sync import idle
import config

def sync_time():
    """مزامنة الوقت لتجنب أخطاء BadMsgNotification[16]."""
    try:
        sys_platform = platform.system().lower()
        if "windows" in sys_platform:
            subprocess.run(["sc", "start", "w32time"], capture_output=True)
            subprocess.run(["w32tm", "/resync", "/force"], capture_output=True)
        else:
            subprocess.run(["sudo", "timedatectl", "set-ntp", "true"], capture_output=True)
    except Exception as e:
        print(f"[WARN]: فشل مزامنة الوقت -> {e}")

# إنشاء البوت باستخدام بيانات الكونفيج
bot = Client(
    "MusicBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins={"root": "Maker"}
)

async def notify_owners(message: str):
    """إرسال رسالة للمالكين مع حماية من أي خطأ."""
    if hasattr(config, "OWNER") and isinstance(config.OWNER, list):
        for owner_id in config.OWNER:
            try:
                await bot.send_message(owner_id, message)
            except Exception as e:
                print(f"[WARN]: لم يتم إرسال الرسالة للمالك {owner_id} -> {e}")

async def start_bot():
    print("[INFO]: بدء تشغيل البوت...")
    await bot.start()
    await notify_owners("✅ البوت الآن يعمل.")
    print("[INFO]: البوت يعمل الآن.")
    await idle()  # البوت يظل شغال

if __name__ == "__main__":
    sync_time()
    try:
        asyncio.run(start_bot())
    except Exception as e:
        print(f"[ERROR]: {e}")
