import os
from os import getenv
from dotenv import load_dotenv

# تحميل متغيرات البيئة من local.env لو موجود
if os.path.exists("local.env"):
    load_dotenv("local.env")
load_dotenv()

# -------------------- #
#    إعدادات البوت     #
# -------------------- #

OWNER = [7971172355]              # أيدي المالكين
OWNER_NAME = "Malak"              # اسم المالك
BOT_TOKEN = "8004105398:AAEXMJPdaotBgfrtVI0aRRb34z5kCHzUqcA"  # توكن البوت

# قاعدة بيانات MongoDB
MONGO_DB_URI = "mongodb+srv://m7921742:<db_password>@cluster0.ege7thr.mongodb.net/"

# API لتليجرام
API_ID = int(getenv("API_ID", "22590972"))
API_HASH = getenv("API_HASH", "cda32c4a768e077caff7469853807bcc")

# روابط القناة والجروب الافتراضية
CHANNEL = "https://t.me/PO_0O"
GROUP = "https://t.me/PO_0O"

# وسائط افتراضية للبوت
VIDEO = "https://telegra.ph/file/770e2d5df0b50264097b2.jpg"
LOGS = "@VDRTM"

# أيدي المالك الأول (للاستخدام المباشر)
OWNER_ID = OWNER[0]

# -------------------- #
#   Dictionaries لتخزين الـ Clients والبيانات
# -------------------- #
appp = {}        # لتخزين App Clients
user = {}        # لتخزين Userbot Clients
helper = {}      # لمساعدات إضافية إذا استخدمت
call = {}        # لتخزين PyTgCalls لكل بوت
dev = {}         # لتخزين Developer IDs
devname = {}     # لتخزين أسماء المطورين
logger = {}      # لتخزين Logger لكل بوت
logger_mode = {} # لتخزين وضع Logger لكل بوت
botname = {}     # لتخزين أسماء البوتات بشكل ديناميكي
must = {}        # لتخزين حالة الاشتراك الإجباري لكل بوت

# -------------------- #
#   إعدادات MongoDB إضافية
# -------------------- #
Bots = None      # سيتم تهيئتها عند الاتصال بـ MongoDB
channeldb = None
groupdb = None
channeldbsr = None
groupdbsr = None
mustdb = None
