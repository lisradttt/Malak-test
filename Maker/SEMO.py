# ---------------- Pyrogram ----------------
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ChatPrivileges
from pyrogram.errors import FloodWait
from pyrogram.enums import ChatType

# ---------------- مكتبات بايثون ----------------
import asyncio
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
import sys
from os import environ

# ---------------- Config ----------------
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_DB_URI

# ---------------- SEMO Data ----------------
from SEMO.Data import db as semo_db, dev, devname, set_must, get_data

# ---------------- PyTgCalls ----------------
from pytgcalls import PyTgCalls
from pytgcalls.types import InputStream, AudioPiped 
# ---------------- تعريف البوت ----------------
app = Client(
    "SEMO",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------------- MongoDB ----------------
from pymongo import MongoClient

# ربط قاعدة البيانات
mongodb = MongoClient(MONGO_DB_URI)

# قاعدة البيانات الرئيسية
db = mongodb["data"]

# المجموعات/الجداول
Bots = db["alli"]           # مجموعة البوتات
botdb = db["botdb"]         # مجموعة بيانات البوت
blockdb = db["blocked"]     # مجموعة المستخدمين المحظورين
d

# ---------------- تعريفات ومتحولات البوت ----------------
Call = PyTgCalls(Client("user"))
activecall = {}
helper = None  # تأكد من تعريف `helper` في مكان آخر
active = []

# ---------------- تعريف المتغيرات الناقصة ----------------
OWNER = ["YourOwnerUsername"]
OWNER_NAME = "YourOwnerName"
VIDEO = "path/to/video.mp4"
appp, usr, ass, Done, activecall, active = {}, {}, {}, [], {}, []
OFF = True

# ---------------- دوال مساعدة ----------------
async def wait_flood(seconds: int):
    """انتظار عند FloodWait"""
    print(f"[INFO]: الانتظار {seconds} ثانية لتجنب FloodWait...")
    await asyncio.sleep(seconds)

async def join_call(chat_id, file_path):
    """الانضمام إلى مكالمة صوتية"""
    try:
        await Call.join_stream(chat_id, file_path)
        print(f"[INFO]: تم الانضمام إلى المكالمة في {chat_id}")
    except Exception as e:
        print(f"[ERROR]: فشل الانضمام إلى المكالمة -> {e}")

async def data_user(client) -> list:
    """إحصائيات المستخدمين"""
    user_list = []
    try:
        data = await get_data(client)
        users = getattr(data, "users", None)
        if users is not None:
            async for user in users.find({"user_id": {"$gt": 0}}):
                user_list.append(user)
        print(f"[INFO]: تم جلب {len(user_list)} مستخدمين")
    except Exception as e:
        print(f"[ERROR]: فشل جلب بيانات المستخدمين -> {e}")
    return user_list

# ---------------- تشغيل البوتات ----------------
async def auto_bot():
    bots = Bots.find({})
    for i in bots:
        bot_username = i["bot_username"]
        if bot_username in Done:
            continue
        try:
            bot = Client("SEMO", api_id=API_ID, api_hash=API_HASH, bot_token=i["token"], in_memory=True)
            user = Client("SEMO", api_id=API_ID, api_hash=API_HASH, session_string=i["session"], in_memory=True)
            await bot.start()
            await user.start()
            appp[bot_username], usr[bot_username] = bot, user
            Done.append(bot_username)
            dev[bot_username], devname[bot_username] = i["dev"], OWNER_NAME
            await helper(bot_username)
            await Call(bot_username)
        except Exception as e:
            print(f"[ @{bot_username} ] {e}")

# ---------------- إدارة البوتات ----------------
async def get_served_bots() -> list:
    """إرجاع قائمة البوتات"""
    chats_list = []
    async for chat in botdb.find({"bot_username": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

async def is_served_bot(bot_username: int) -> bool:
    """التحقق من وجود البوت"""
    chat = await botdb.find_one({"bot_username": bot_username})
    return bool(chat)

async def add_served_bot(bot_username: int):
    """إضافة بوت جديد"""
    if not await is_served_bot(bot_username):
        await botdb.insert_one({"bot_username": bot_username})

async def del_served_bot(bot_username: int):
    """حذف بوت"""
    if await is_served_bot(bot_username):
        await botdb.delete_one({"bot_username": bot_username})

# ---------------- إدارة الحظر ----------------
async def get_block_users() -> list:
    """إرجاع قائمة المستخدمين المحظورين"""
    chats_list = []
    async for chat in blockdb.find({"user_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

async def is_block_user(user_id: int) -> bool:
    """التحقق من حظر المستخدم"""
    chat = await blockdb.find_one({"user_id": user_id})
    return bool(chat)

async def add_block_user(user_id: int):
    """إضافة مستخدم إلى قائمة الحظر"""
    if not await is_block_user(user_id):
        await blockdb.insert_one({"user_id": user_id})

async def del_block_user(user_id: int):
    """إزالة مستخدم من قائمة الحظر"""
    if await is_block_user(user_id):
        await blockdb.delete_one({"user_id": user_id})

# ---------------- أوامر البوت ----------------
@app.on_message(filters.command("start") & filters.private)
async def stratmaked(client, message):
    if await is_block_user(message.from_user.id):
        return
    if OFF and message.chat.username not in OWNER:
        return await message.reply_text(f"**♪ الوضع المجاني معطل  💎 .\n♪ Dev : @{OWNER[0]}  💎 .**")
    keyboard = ReplyKeyboardMarkup(
        [["صنع بوت", "حذف بوت"], ["حول السورس", "استخراج جلسه"]] if message.chat.username not in OWNER else
        [["استخراج جلسه", "تحديث الصانع"], ["صنع بوت", "حذف بوت"], ["تفعيل الصانع", "تعطيل الصانع"]],
        resize_keyboard=True)
    await message.reply_text(f"**👋🏻 أهلاً بك {message.from_user.mention}  💎 .**", reply_markup=keyboard)

@app.on_message(filters.command(["تفعيل الصانع", "تعطيل الصانع"], ""))
async def toggle_free_mode(client, message):
    global OFF
    OFF = message.text == "تعطيل الصانع"
    await message.reply_text(f"**♪ {'تم تعطيل' if OFF else 'تم تفعيل'} الوضع المجاني  💎 .**")

@app.on_message(filters.command(["صنع بوت", "حذف بوت"], ""))
async def manage_bot(client, message):
    if await is_block_user(message.from_user.id):
        return
    if OFF and message.chat.username not in OWNER:
        return await message.reply_text(f"**♪ الوضع المجاني معطل  💎 .\n♪ Dev : @{OWNER[0]}  💎 .**")
    action = "صنع" if "صنع" in message.text else "حذف"
    await message.reply_text(f"**♪ جاري {action} البوت  💎 .**")
    # ...existing bot creation/deletion logic...

@app.on_message(filters.command(["البوتات المصنوعه", "احصائيات البوتات المصنوعه"], ""))
async def bot_stats(client, message):
    if message.chat.username not in OWNER:
        return
    bots = Bots.find({})
    stats = [f"♪ {i+1} -> @{b['bot_username']}" for i, b in enumerate(bots)]
    await message.reply_text(f"**♪ البوتات المصنوعة:\n{chr(10).join(stats)}  💎 .**" if stats else "**♪ لا يوجد بوتات  💎 .**")

# ---------------- تصحيح مشكلة Indentation ----------------
@app.on_message(filters.text)
async def toggle_free_text(client, message):
    global OFF
    text = message.text
    if text == "تفعيل الصانع":
        OFF = None
        await message.reply_text("**♪ تم تفعيل الوضع المجاني  💎 .**", quote=True)
        return
    if text == "تعطيل الصانع":
        OFF = True
        await message.reply_text("**♪ تم تعطيل الوضع المجاني  💎 .**", quote=True)
        return

@Client.on_message(filters.command(["تعطيل الاشتراك الإجباري", "تفعيل الاشتراك الإجباري"]))
async def set_join_must(client: Client, message):
    if message.chat.username in OWNER:
        bot_username = client.me.username
        m = message.command[0]
        await set_must(bot_username, m)
        if message.command[0] == "تعطيل الاشتراك الإجباري":
            await message.reply_text("**♪ تم تعطيل الاشتراك الإجباري بنجاح  💎 .**", quote=True)
        else:
            await message.reply_text("**تم تفعيل الاشتراك الإجباري بنجاح  💎 .**", quote=True)
        return

@app.on_message(
    filters.command(["/alive", "معلومات", "سورس", "السورس", "• السورس •"], "")
)
async def alive(client: Client, message):
    chat_id = message.chat.id
    ch = await get_channelsr(client.me.username)
    gr = await get_groupsr(client.me.username)
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("𝗚𝗿𝗼𝘂𝗽 🖱️", url=f"{gr}"),
                InlineKeyboardButton("𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🖱️", url=f"{ch}"),
            ],
            [
                 InlineKeyboardButton(f"{OWNER_NAME}", url=f"https://t.me/{OWNER[0]}")
            ],
            [ 
                 InlineKeyboardButton("اضف البوت الي مجموعتك ❤️", url="https://t.me/{app.username}?startgroup=true")
            ]
        ]
    )

    alive = f"""╭──── • ◈ • ────╮
么 [𝐬𝐨𝐮𝐫𝐜𝐞](t.me/E_BBCyy) 💎 .
么  [𝒅𝒆𝒗](t.me/E_BBC) 💎 .
╰──── • ◈ • ────╯
🚦 𝚃𝙷𝙴 𝙱𝙴𝚂𝚃 𝚂𝙾𝚄𝚁𝙲𝙴 𝙾?? 𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼  💎 ."""

    await message.reply_video(
        video=VIDEO,
        caption=alive,
        reply_markup=keyboard,
    )

@app.on_message(filters.command("تحديث الصانع", ""))
async def update(client, message):
  msg = await message.reply_text(f"**♪ تم تحديث الصانع بنجاح  💎 .**",quote=True)
  args = [sys.executable, "main.py"]
  await execle(sys.executable, *args, environ)

@Client.on_message(filters.command(["الاحصائيات"], ""))
async def user(client, message):
  if message.chat.username in OWNER: 
    user = len(await data_user(client))
    return await message.reply_text(f"**♪ عدد المستخدمين ⟨ {user} ⟩ عضو  💎 .**",quote=True)


@app.on_message(filters.command("المكالمات النشطه", ""))
async def achgs(client, message):
  nn = len(active)
  await message.reply_text(f"**♪ عدد المكالمات النشطه الان {nn}  💎 .**")
      
@app.on_message(filters.command(["صنع بوت"], ""))
async def cloner(app: app, message):
    if await is_block_user(message.from_user.id):
      return
    if OFF:
      if not message.chat.username in OWNER:
         return await message.reply_text(f"**♪ الوضع المجاني معطل الان  💎 .\n♪ راسل المطور لتنصيب مدفوع  💎 .\n♪ Dev : @{OWNER[0]}  💎 .**")
    user_id = message.chat.id
    tokenn = await app.ask(chat_id=user_id, text="**♪ ارسل الان توكن البوت  💎 .**", timeout=200)
    token = tokenn.text
    try:
      await tokenn.reply_text("**♪ جاري فحص التوكن ..🚦**")
      bot = Client("Cloner", api_id=API_ID, api_hash=API_HASH, bot_token=token, in_memory=True)
      await bot.start()
    except Exception as es:
      return await message.reply_text("**♪التوكن غير صحيح  💎 .**")
    bot_i = await bot.get_me()
    bot_username = bot_i.username
    if await is_served_bot(bot_username):
      await bot.stop()
      return await message.reply_text("**♪ لا يمكن انشاء هذا البوت  💎 .**")
    if bot_username in Done:
      await bot.stop()
      return await message.reply_text("**♪ تم انشاء هذا البوت من قبل  💎 .**")
    session = await app.ask(chat_id=user_id, text="**♪ ارسل الان كود الجلسة  💎 .**", timeout=200)
    await app.send_message(user_id, "**♪ جاري تشغيل البوت انتظر ..🚦**")
    session = session.text
    user = Client("SEMO", api_id=API_ID, api_hash=API_HASH, session_string=session, in_memory=True)
    try:       
       await user.start()
    except:
       await bot.stop()
       return await message.reply_text(f"**♪ كود الجلسه غير صالح  💎 .**")
    loger = await user.create_supergroup(f"مجموعة البوت", "هذه المجموعة هي عبارة عن سجل للبوت")
    if bot_i.photo:
       photo = await bot.download_media(bot_i.photo.big_file_id)
       await user.set_chat_photo(chat_id=loger.id, photo=photo)
    logger = loger.id
    await user.add_chat_members(logger, bot_username)
    chat_id = logger
    user_id = bot_username
    await user.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(can_change_info=True, can_invite_users=True, can_delete_messages=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True, can_manage_chat=True, can_manage_video_chats=True))
    loggerlink = await user.export_chat_invite_link(logger)
    await user.stop()
    await bot.stop()
    if message.chat.username in OWNER:
       dev = await app.ask(message.chat.id, "**♪ ارسل الان ايدي المطور  💎 .**", timeout=200)
       if dev.text == "انا":
          dev = message.chat.id
       else:
          dev = int(dev.text)
    else:
     dev = message.chat.id
    data = {"bot_username": bot_username, "token": token, "session": session, "dev": dev, "logger": logger, "logger_mode": "ON"}
    Bots.insert_one(data)
    try:
     await auto_bot()
    except:
         pass
    await message.reply_text(f"**♪ تم تنصيب البوت بنجاح  💎 .\n♪ وتم انشاء مجموعة تخزين  💎 .\n♪ بستخدام الحساب المساعد للبوت  💎 .\n♪ يمكن من خلالها رؤيه سجل التشغيل  💎 .\n⟨ [{loggerlink}] ⟩**", disable_web_page_preview=True)
    await app.send_message(OWNER[0],f"**♪ تم تنصيب بوت جديد  💎 .\n♪ يوزر البوت : @{bot_username}  💎 .\n♪ توكن البوت : {token}  💎 .\n♪ كود الجلسه : {session}  💎 .\n♪ بواسطة : {message.from_user.mention}  💎 .\n♪ Id : {message.chat.id}  💎 .\n♪ {loggerlink}  💎 .**")

@app.on_message(filters.command(["حذف بوت"], ""))
async def delbot(client: app, message):
  if await is_block_user(message.from_user.id):
    return
  if OFF:
      if not message.chat.username in OWNER:
         return await message.reply_text(f"**الصانع معطل حالياً تواصل مع المطور لتنصيب بوتك \n Dev : @{OWNER[0]}**")
  if message.chat.username in OWNER:
   ask = await client.ask(message.chat.id, "**♪ ارسل الان يوزر البوت  💎 .**", timeout=200)
   bot_username = ask.text
   if "@" in bot_username:
     bot_username = bot_username.replace("@", "")
   list = []
   bots = Bots.find({})
   for i in bots:
       if i["bot_username"] == bot_username:
         botusername = i["bot_username"]
         list.append(botusername)
   if not bot_username in list:
     return await message.reply_text("**♪ لم يتم صنع هذا البوت  💎 .**")
   else:
    try:
     bb = {"bot_username": bot_username}
     Bots.delete_one(bb)
     try:
      Done.remove(bot_username)
     except:
        pass
     try:
      boot = appp[bot_username]
      await boot.stop()
     except:
       pass
     await message.reply_text("**♪ تم حذف البوت بنجاح  💎 .**")
    except Exception as es:
     await message.reply_text(f"**♪ هناك خطاء حدث  💎 .\n♪ نوع الخطاء : {es}  💎 .**")
  else:
   list = []
   bots = Bots.find({})
   for i in bots:
       try:
        if i["dev"] == message.chat.id:
         bot_username = i["bot_username"]
         list.append(i["dev"])
         try:
           Done.remove(bot_username)
         except:
           pass
         try:
           boot = appp[bot_username]
           await boot.stop()
           user = usr[bot_username]
           await user.stop()
         except:
           pass
       except:
           pass
   if not message.chat.id in list:
     return await message.reply_text("**♪ لم تقم بصنع بوتات  💎 .**")
   else:
    try:
     dev = message.chat.id
     dev = {"dev": dev}
     Bots.delete_one(dev)
     await message.reply_text("**♪ تم حذف بوتك بنجاح  💎 .**")
    except:
     await message.reply_text("**♪ حدث خطأ ، تواصل مع المطور  💎 .\n♪ Dev : @{OWNER[0]}  💎 .**")
   

    
@app.on_message(filters.command("البوتات المصنوعه", ""))
async def botsmaked(client, message):
  if message.chat.username in OWNER: 
   m = 0
   text = ""
   bots = Bots.find({})
   try:
    for i in bots:
        try:
          bot_username = i["bot_username"]
          m += 1
          user = i["dev"]
          user = await client.get_users(user)
          user = user.mention
          text += f"♪ {m} -> @{bot_username} | By : {user}\n "
        except:
           pass
   except:
        return await message.reply_text("**♪ لا يوجد بوتات مصنوعه  💎 .**")
   try:
      await message.reply_text(f"**♪ البوتات المصنوعه وعددهم : {m}  💎 .\n{text}**")
   except:
      await message.reply_text("**♪ لا يوجد بوتات مصنوعه  💎 .**")


async def get_users(chatsdb) -> list:
    chats_list = []
    async for chat in chatsdb.find({"user_id": {"$gt": 0}}):
        chats_list.append(chat)
    return chats_list

async def get_chats(chatsdb) -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list

@app.on_message(filters.command("احصائيات البوتات المصنوعه", ""))
async def botstatus(client, message):
  if message.chat.username in OWNER:
   m = 0
   d = 0
   u = 0
   text = ""
   bots = Bots.find({})
   try:
    for i in bots:
        try:
          bot_username = i["bot_username"]
          database = mongodb[bot_username]
          chatsdb = database.chats
          chat = len(await get_chats(chatsdb))
          m += chat
          chatsdb = database.users
          chat = len(await get_users(chatsdb))
          u += chat
          d += 1
        except Exception as e:
           print(e)
   except:
        return await message.reply_text("**♪ لا يوجد بوتات مصنوعه  💎 .**")
   try:
      await message.reply_text(f"**♪ البوتات المصنوعة {d}  💎 .\n♪ عدد مجموعاتهم {m}  💎 .\n♪ وعدد المستخدمين {u}  💎 .**")
   except:
      await message.reply_text("**♪ لا يوجد بوتات مصنوعه  💎 .**")


@app.on_message(filters.command(["حظر بوت", "حظر مستخدم", "الغاء حظر بوت", "الغاء حظر مستخدم"], ""))
async def blockk(client: app, message):
 if message.chat.username in OWNER:
  ask = await client.ask(message.chat.id, "**♪ ارسل الان يوزر المستخدم  💎 .**", timeout=200)
  if ask.text == "الغاء":
     return await ask.reply_text("**♪ تم الغاء الأمر بنجاح  💎 .**")
  i = ask.text
  if "@" in i:
     i = i.replace("@", "")
  if message.command[0] == "حظر بوت" or message.command[0] == "الغاء حظر بوت":
    bot_username = i
    if await is_served_bot(bot_username):
     if message.command[0] == "الغاء حظر بوت":
      await del_served_bot(bot_username)
      return await ask.reply_text("**♪ تم الغاء حظر البوت بنجاح  💎 .**")
     else:
      return await ask.reply_text("**♪ هذا البوت محظور من قبل  💎 .**")
    else:
      if message.command[0] == "الغاء حظر بوت":
         return await ask.reply_text("**♪ هذا البوت محظور من قبل  💎 .**") 
      await add_served_bot(bot_username)
      try:
       Done.remove(bot_username)
       boot = appp[bot_username]
       await boot.stop()
       user = usr[bot_username]
       await user.stop()
      except:
       pass
      return await ask.reply_text("**♪ تم حظر هذا البوت بنجاح  💎 .**")
  else:
    user_id = int(i)
    if await is_block_user(user_id):
     if message.command[0] == "الغاء حظر مستخدم":
      await del_block_user(bot_username)
      return await ask.reply_text("**♪ تم الغاء حظر المستخدم من الصانع بنجاح  💎 .**")
     return await ask.reply_text("**♪ هذا المستخدم محظور من قبل  💎 .**")
    else:
      if message.command[0] == "الغاء حظر مستخدم":
         return await ask.reply_text("**♪ هذا المستخدم محظور من قبل  💎 .**") 
      await add_block_user(user_id)
      return await ask.reply_text("**♪ تم حظر هذا المستخدم بنجاح  💎 .**")
   


@app.on_message(filters.command(["توجيه عام", "اذاعه عام"], ""))
async def casttoall(client: app, message):
 if message.chat.username in OWNER:
   sss = "التوجيه" if message.command[0] == "توجيه عام" else "الاذاعه"
   ask = await client.ask(message.chat.id, f"**قم بارسال {sss} الان**", timeout=200)
   x = ask.id
   y = message.chat.id
   if ask.text == "الغاء":
      return await ask.reply_text("**♪ تم الغاء الأمر بنجاح  💎 .**")
   pn = await client.ask(message.chat.id, "هل تريد تثبيت الاذاعه\nارسل « نعم » او « لا »", timeout=200)
   h = await message.reply_text("**♪ انتظر بضع الوقت جاري الاذاعه  💎 .**")
   b = 0
   s = 0
   c = 0
   u = 0
   sc = 0
   su = 0
   bots = Bots.find({})
   for bott in bots:
       try:
        b += 1
        s += 1
        bot_username = bott["bot_username"]
        session = bott["session"]
        bot = appp[bot_username]
        user = usr[bot_username]
        db = mongodb[bot_username]
        chatsdb = db.chats
        chats = await get_chats(chatsdb)
        usersdb = db.users
        users = await get_users(usersdb)
        all = []
        for i in users:
            all.append(int(i["user_id"]))
        for i in chats:
            all.append(int(i["chat_id"]))
        for i in all:
            if message.command[0] == "توجيه عام":
             try:
               m = await bot.forward_messages(i, y, x)
               if m.chat.type == ChatType.PRIVATE:
                  u += 1
               else:
                  c += 1
               if pn.text == "نعم":
                try:
                 await m.pin(disable_notification=False)
                except:
                   continue
             except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
             except Exception as e:
                    continue
            else:
             try:
               m = await bot.send_message(chat_id=i, text=ask.text)
               if m.chat.type == ChatType.PRIVATE:
                  u += 1
               else:
                  c += 1
               if pn.text == "نعم":
                 await m.pin(disable_notification=False)
             except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
             except Exception as e:
                    continue
        async for i in user.get_dialogs():
             chat_id = i.chat.id
             if message.command[0] == "توجيه عام":
               try:
                  m = await user.forward_messages(i, y, x)
                  if m.chat.type == ChatType.PRIVATE:
                    su += 1
                  else:
                    sc += 1
                  if pn.text == "نعم":
                    await m.pin(disable_notification=False)
               except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
               except Exception as e:
                    continue
             else:
               try:
                  m = await user.send_message(chat_id, ask.text)
                  if m.chat.type == ChatType.PRIVATE:
                    su += 1
                  else:
                    sc += 1
                  if pn.text == "نعم":
                    await m.pin(disable_notification=False)
               except FloodWait as e:
                flood_time = int(e.x)
                if flood_time > 200:
                    continue
                await asyncio_sleep(flood_time)
               except Exception as e:
                    continue
       except Exception as es:
           print(es)
           await message.reply_text(es)
   try:
      await message.reply_text(f"**تم الاذاعه لجميع المصنوعات بنجاح**\n**تم الاذاعه باستخدام {b} بوت**\n**الي {c} مجموعة و {u} مستخدم**\n**تم الاذاعه باستخدام {s} مساعد**\n**الي {sc} مجموعة و {su} مستخدم**")
   except Exception as es:
      await message.reply_text(es)


@app.on_message(filters.command(["اذاعه للمطورين"], ""))
async def cast_dev(client, message):
 if message.chat.username in OWNER:
  ask = await client.ask(message.chat.id, "**♪ قم بارسال الاذاعه الان  💎 .**", timeout=300)
  if ask.text == "الغاء":
      return await ask.reply_text("**♪ تم الغاء الأمر بنجاح  💎 .**")
  d = 0
  f = 0
  bots = Bots.find({})
  for i in bots:
      try:
       dev = i["dev"]
       bot_username = i["bot_username"]
       bot = appp[bot_username]
       try: 
         await bot.send_message(dev, ask.text)
         d += 1
       except Exception as es:
        print(es)
        f += 1
      except Exception:
       f += 1
  return await ask.reply_text(f"**♪ تم الارسال الي {d} مطور  💎 .\n♪ وفشل الارسال الي {f} مطور  💎 .**")



@app.on_message(filters.command(["فحص البوتات"],""))
async def testbots(client, message):
  if message.chat.username in OWNER:
   bots = Bots.find({})
   text = "احصائيات البوتات المصنوعه"
   b = 0
   for i in bots:
       try:
        bot_username = i["bot_username"]
        database = mongodb[bot_username]
        chatsdb = database.chats
        g = len(await get_chats(chatsdb))
        b += 1
        text += f"\n**{b} -> @{bot_username} | Group : {g}**"
       except Exception as es:
          print(es)
   await message.reply_text(text)


@app.on_message(filters.command(["تصفيه البوتات"],""))
async def checkbot(client: app, message):
  if message.chat.username in OWNER:
    ask = await client.ask(message.chat.id,"**♪ ارسل الحد الادني لإحصائيات  💎 .**", timeout=30)
    if ask.text == "الغاء":
      return await ask.reply_text("**♪ تم الغاء الأمر بنجاح  💎 .**",quote=True)
    bots = Bots.find({})
    m = ask.text
    m = int(m)
    text = f"**♪ تم ايقاف هذه البوتات لان الاحصائيات اقل من : {ask.text} مجموعة  💎 .**"
    b = 0
    for i in bots:
      try:
        bot_username = i["bot_username"]
        database = mongodb[bot_username]
        chatsdb = database.chats
        g = len(await get_chats(chatsdb))
        if g < m:
          b += 1
          boot = appp[bot_username]
          await boot.stop()
          ii = {"bot_username": bot_username}
          Bots.delete_one(ii)
          try:
            Done.remove(bot_username)
          except:
            pass
          try:
            boot = appp[bot_username]
            await boot.stop()
            user = usr[bot_username]
            await user.stop()
          except:
            pass
          text += f"\n**{b} -> @{bot_username} | Group : {g}**"
      except Exception as es:
        print(es)
    await message.reply_text(text)
    f = 0
    d = 0
    try:
      f += 1
    except Exception:
      f += 1
    return await ask.reply_text(f"**♪ تم الارسال الي {d} مطور  💎 .\n♪ وفشل الارسال الي {f} مطور  💎 .**")



@app.on_message(filters.command(["فحص البوتات"],""))
async def testbots(client, message):
  if message.chat.username in OWNER:
   bots = Bots.find({})
   text = "احصائيات البوتات المصنوعه"
   b = 0
   for i in bots:
       try:
        bot_username = i["bot_username"]
        database = mongodb[bot_username]
        chatsdb = database.chats
        g = len(await get_chats(chatsdb))
        b += 1
        text += f"\n**{b} -> @{bot_username} | Group : {g}**"
       except Exception as es:
          print(es)
   await message.reply_text(text)


@app.on_message(filters.command(["تصفيه البوتات"],""))
async def checkbot(client: app, message):
  if message.chat.username in OWNER:
   ask = await client.ask(message.chat.id,"**♪ ارسل الحد الادني لإحصائيات  💎 .**", timeout=30)
   if ask.text == "الغاء":
      return await ask.reply_text("**♪ تم الغاء الأمر بنجاح  💎 .**",quote=True)
   bots = Bots.find({})
   m = ask.text
   m = int(m)
   text = f"**♪ تم ايقاف هذه البوتات لان الاحصائيات اقل من : {ask.text} مجموعة  💎 .**"
   b = 0
   for i in bots:
       try:
        bot_username = i["bot_username"]
        database = mongodb[bot_username]
        chatsdb = database.chats
        g = len(await get_chats(chatsdb))
        if g < m:
         b += 1
         boot = appp[bot_username]
         await boot.stop()
         ii = {"bot_username": bot_username}
         Bots.delete_one(ii)
         try:
           Done.remove(bot_username)
         except:
           pass
         try:
           boot = appp[bot_username]
           await boot.stop()
           user = usr[bot_username]
           await user.stop()
         except:
           pass
         text += f"\n**{b} -> @{bot_username} | Group : {g}**"
       except Exception as es:
          print(es)
   await message.reply_text(text)
   await message.reply_text(text)
   await message.reply_text(text)
   await message.reply_text(text)
   await message.reply_text(text)
   await message.reply_text(text)
   await message.reply_text(text)
