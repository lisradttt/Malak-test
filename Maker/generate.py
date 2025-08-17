# ---------------- Python ----------------
import asyncio
import os
from os import getenv
from asyncio.exceptions import TimeoutError

# ---------------- Pyrogram ----------------
from pyrogram.client import Client  # type: ignore
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from pyrogram.enums import ChatType

# ---------------- Telethon ----------------
from telethon.client import TelegramClient  # type: ignore
from telethon.sessions import StringSession
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)
from telethon import Button  # type: ignore

# ---------------- Config ----------------
import config

# ---------------- محتوى البوت ----------------
ask_ques = "**♪ قم بالضغط علي زر بيروجرام  💎 .**"
buttons_ques = [
    [InlineKeyboardButton("بيروجرام", callback_data="pyrogram")]
]

gen_button = [
    [InlineKeyboardButton("♪ استخراج جلسه  💎 .", callback_data="generate")]
]

# ---------------- إنشاء Client ----------------
app = Client("my_bot", api_id=config.API_ID, api_hash=config.API_HASH)  # type: ignore

# ---------------- handlers ----------------
@app.on_message(filters.private & ~filters.forwarded & filters.command(["استخراج جلسه", ": استخراج جلسه :"], prefixes=""))  # type: ignore
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))

# ---------------- دالة cancelled ----------------
async def cancelled(msg: Message):
    text = msg.text
    if text in ["/cancel", "/restart"] or text.startswith("/"):
        await msg.reply("**» العملية تم إيقافها !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif text == "/skip":
        return False
    return False

# ---------------- دالة استخراج الجلسة ----------------
async def generate_session(bot: Client, msg: Message, telethon: bool = False, is_bot: bool = False):
    user_id = msg.chat.id
    await msg.reply("**♪ انت الان سوف تستخرج جلسه بيروجرام اصدار 2.0.59  💎 .**")

    # الحصول على api_id و api_hash
    api_id_msg = await bot.ask(user_id, "**♪ ارسل الان : api_id الخاص بالحساب  💎 .**", filters=filters.text)  # type: ignore
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "تخطي":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**ᴀᴩɪ_ɪᴅ** ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "**ارسل الان : api_hash الخاص بالحساب  💎 .**", filters=filters.text)  # type: ignore
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text

    # رقم الهاتف أو توكن البوت
    if not is_bot:
        t = "**♪ حسنا ارسل الان رقم حسابك  💎 .\n♪ مثل : +201012345678  💎 .**"
    else:
        t = "ᴩʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ʙᴏᴛ_ᴛᴏᴋᴇɴ** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.\nᴇxᴀᴍᴘʟᴇ : `5432198765:abcdanonymousterabaaplol`'"

    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)  # type: ignore
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text

    if not is_bot:
        await msg.reply("**♪ جاري ارسال الكود الي حسابك ..🚦**")
    else:
        await msg.reply("» ᴛʀʏɪɴɢ ᴛᴏ ʟᴏɢɪɴ ᴠɪᴀ ʙᴏᴛ ᴛᴏᴋᴇɴ...")

    # إنشاء client المناسب
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)  # type: ignore
        await client.start()  # type: ignore
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)  # type: ignore
        await client.start()  # type: ignore
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)  # type: ignore
        await client.start()  # type: ignore

    # إرسال كود التحقق إذا حساب عادي
    if not is_bot:
        try:
            if telethon:
                await client.send_code_request(phone_number)  # type: ignore
            else:
                await client.send_code(phone_number)  # type: ignore
        except (ApiIdInvalid, ApiIdInvalidError):
            await msg.reply("» ʏᴏᴜʀ **ᴀᴩɪ_ɪᴅ** ᴏʀ **ᴀᴩɪ_ʜᴀsʜ** غير صحيحة.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneNumberInvalid, PhoneNumberInvalidError):
            await msg.reply("» رقم الهاتف غير صحيح.", reply_markup=InlineKeyboardMarkup(gen_button))
            return

    # استلام كود التحقق
    if not is_bot:
        try:
            phone_code_msg = await bot.ask(user_id, "♪ قم بكتابة الكود المستلم  💎 .", filters=filters.text, timeout=600)  # type: ignore
            if await cancelled(phone_code_msg):
                return
            phone_code = phone_code_msg.text.replace(" ", "")
            if telethon:
                await client.sign_in(phone_number, phone_code)  # type: ignore
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)  # type: ignore
        except TimeoutError:
            await msg.reply("**♪ لقد تاخرت في ارسال الكود  💎 .**", reply_markup=InlineKeyboardMarkup(gen_button))
            return

    # استخراج الجلسة وإرسالها
    string_session = client.session.save() if telethon else await client.export_session_string()  # type: ignore
    text = f"**♪ تم استخراج الجلسه بنجاح  💎 .** \n\n`{string_session}`\n\n**♪ اضغط لنسخ الجلسه  💎 .**"
    await bot.send_message(msg.chat.id, text)  # type: ignore

    # فصل العميل
    await client.stop()  # type: ignore
