import asyncio
import platform
import subprocess
import os
from pyrogram.client import Client
from pyrogram.sync import idle
from config import API_ID, API_HASH, BOT_TOKEN, OWNER  # استدعاء المتغيرات مباشرة

SESSION_FILE = "MusicBot.session"
SEMO_FOLDER = "SEMO"

def sync_time():
    """مزامنة الوقت لتجنب BadMsgNotification[16]."""
    try:
        sys_platform = platform.system().lower()
        if "windows" in sys_platform:
            subprocess.run(["sc", "start", "w32time"], capture_output=True)
            subprocess.run(["w32tm", "/resync", "/force"], capture_output=True)
        else:
            subprocess.run(["sudo", "timedatectl", "set-ntp", "true"], capture_output=True)
    except Exception as e:
        print(f"[WARN]: فشل مزامنة الوقت -> {e}")

def ensure_semo_folder():
    """تأكد من وجود فولدر SEMO."""
    if not os.path.exists(SEMO_FOLDER):
        os.makedirs(SEMO_FOLDER)
        print(f"[INFO]: تم إنشاء فولدر المصنوع {SEMO_FOLDER}")

def ensure_session():
    """تأكد من وجود جلسة صالحة، وإعادة إنشاء جديدة إذا كانت قديمة."""
    if not os.path.exists(SESSION_FILE):
        print("[INFO]: لم يتم العثور على جلسة سابقة، سيتم إنشاء جلسة جديدة عند التشغيل.")
    else:
        print("[INFO]: تم العثور على جلسة موجودة، سيتم استخدامها.")

# إنشاء البوت باستخدام بيانات الكونفيج
bot = Client(
    SESSION_FILE,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "Maker"}
)

async def notify_owners(message: str):
    """إرسال رسالة للمالكين مع حماية من أي خطأ."""
    if isinstance(OWNER, list):
        for owner_id in OWNER:
            try:
                await bot.send_message(owner_id, message)
            except Exception as e:
                print(f"[WARN]: لم يتم إرسال الرسالة للمالك {owner_id} -> {e}")

async def start_bot():
    print("[INFO]: بدء تشغيل البوت...")
    await bot.start()
    await notify_owners("✅ البوت الآن يعمل.")
    print("[INFO]: البوت يعمل الآن.")
    ensure_semo_folder()  # تأكد من فولدر SEMO قبل أي عمليات
    await idle()  # البوت يظل شغال

if __name__ == "__main__":
    sync_time()
    ensure_session()
    try:
        asyncio.run(start_bot())
    except Exception as e:
        print(f"[ERROR]: {e}")
