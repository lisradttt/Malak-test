import os
import asyncio

# ---------------- Config ----------------
from config import OWNER, OWNER_NAME, VIDEO

# ---------------- Pyrogram ----------------
from pyrogram.client import Client
from pyrogram import filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message
)

# ---------------- SEMO Modules ----------------
from SEMO.info import remove_active, is_served_call, joinch, add, db, download, gen_thumb
from SEMO.Data import get_call, get_dev, get_group, get_channel

# ---------------- PyTgCalls ----------------
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityAudio,
    LowQualityVideo,
    MediumQualityAudio,
    MediumQualityVideo
)

# ---------------- ثابت الصور ----------------
PHOTO = VIDEO  # صورة افتراضية من الكونفيج

# ---------------- Callback Query Handler ----------------
@Client.on_callback_query(filters.regex(pattern=r"^(pause|skip|stop|resume)$"))
async def admin_risghts(client: Client, callback_query: CallbackQuery):
    try:
        a = await client.get_chat_member(callback_query.message.chat.id, callback_query.from_user.id)
        bot_username = client.me.username
        dev = await get_dev(bot_username)
        if not a.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            if not callback_query.from_user.id == dev:
                if not callback_query.from_user.username in OWNER:
                    return await callback_query.answer("يجب انت تكون ادمن للقيام بذلك  !", show_alert=True)

        command = callback_query.matches[0].group(1)
        chat_id = callback_query.message.chat.id

        if not await is_served_call(client, chat_id):
            return await callback_query.answer("لا يوجد شئ قيد التشغيل الان .", show_alert=True)

        call = await get_call(bot_username)

        if command == "pause":
            await call.pause_stream(chat_id)  # type: ignore
            await callback_query.answer("تم ايقاف التشغيل موقتا ☕🍀", show_alert=True)
            await callback_query.message.reply_text(f"{callback_query.from_user.mention} **تم ايقاف التشغيل بواسطه**")

        if command == "resume":
            await call.resume_stream(chat_id)  # type: ignore
            await callback_query.answer("تم استكمال التشغيل ☕🍀", show_alert=True)
            await callback_query.message.reply_text(f"{callback_query.from_user.mention} **تم إستكمال التشغيل بواسطه**")

        if command == "stop":
            try:
                await call.leave_group_call(chat_id)  # type: ignore
            except:
                pass
            await remove_active(bot_username, chat_id)
            await callback_query.answer("تم انهاء التشغيل بنجاح ⚡", show_alert=True)
            await callback_query.message.reply_text(f"{callback_query.from_user.mention} **تم انهاء التشغيل بواسطه**")
    except:
        pass


# ---------------- Message Handler ----------------
@Client.on_message(
    filters.command(
        ["/stop", "/end", "/skip", "/resume", "/pause", "/loop",
         "ايقاف مؤقت", "استكمال", "تخطي", "انهاء", "اسكت", "ايقاف",
         "تكرار", "كررها"], ""
    ) & ~filters.private
)
async def admin_risght(client: Client, message: Message):
    try:
        if await joinch(message):
            return

        bot_username = client.me.username
        dev = await get_dev(bot_username)

        if not message.chat.type == ChatType.CHANNEL:
            a = await client.get_chat_member(message.chat.id, message.from_user.id)
            if not a.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
                if not message.from_user.id == dev:
                    if not message.from_user.username in OWNER:
                        return await message.reply_text("**يجب انت تكون ادمن للقيام بذلك  !**")

        command = message.command[0]
        chat_id = message.chat.id

        if not await is_served_call(client, chat_id):
            return await message.reply_text("**لا يوجد شئ قيد التشغيل الان .**")

        call = await get_call(bot_username)

        if command in ["/pause", "ايقاف مؤقت"]:
            await call.pause_stream(chat_id)  # type: ignore
            await message.reply_text(f"**تم ايقاف التشغيل موقتاً .♻️**")

        elif command in ["/resume", "استكمال"]:
            await call.resume_stream(chat_id)  # type: ignore
            await message.reply_text(f"**تم إستكمال التشغيل .🚀**")

        elif command in ["/stop", "/end", "اسكت", "انهاء", "ايقاف"]:
            try:
                await call.leave_group_call(chat_id)  # type: ignore
            except:
                pass
            await remove_active(bot_username, chat_id)
            await message.reply_text(f"**تم انهاء التشغيل .**")

        elif command in ["تكرار", "كررها", "/loop"]:
            if len(message.text) == 1:
                return await message.reply_text("**قم بتحديد مرات التكرار ..🖱️**")
            x = message.text.split(None, 1)[1]
            i = x
            if i in ["1","2","3","4","5","6","7","8","9","10"]:
                x = i
                xx = f"{x} مره"
            elif x == "مره":
                x = 1
                xx = "مره واحده"
            elif x == "مرتين":
                x = 2
                xx = "مرتين"
            else:
                return await message.reply_text("**خطأ في استخدام الامر ،**\n**استخدم الامر هكذا « تكرار 1**")
            
            chat = f"{bot_username}{chat_id}"
            check = db.get(chat)
            file_path = check[0]["file_path"]
            title = check[0]["title"]
            duration = check[0]["dur"]
            user_id = check[0]["user_id"]
            chat_id = check[0]["chat_id"]
            vid = check[0]["vid"]
            link = check[0]["link"]
            videoid = check[0]["videoid"]

            for i in range(int(x)):
                file_path = file_path if file_path else None
                await add(chat_id, bot_username, file_path, link, title, duration, videoid, vid, user_id)
            
            await message.reply_text(f"**تم تفعيل التكرار {xx}**")

        elif command in ["/skip", "تخطي"]:
            chat = f"{bot_username}{chat_id}"
            check = db.get(chat)
            popped = check.pop(0)

            if not check:
                await call.leave_group_call(chat_id)  # type: ignore
                await remove_active(bot_username, chat_id)
                return await message.reply_text("**تم ايقاف التشغيل لأن قائمة التشغيل فارغة .⚡**")

            file = check[0]["file_path"]
            title = check[0]["title"]
            dur = check[0]["dur"]
            video = check[0]["vid"]
            videoid = check[0]["videoid"]
            user_id = check[0]["user_id"]
            link = check[0]["link"]

            audio_stream_quality = MediumQualityAudio()
            video_stream_quality = MediumQualityVideo()

            if file:
                file_path = file
            else:
                try:
                    file_path = await download(bot_username, link, video)
                except:
                    return await client.send_message(chat_id, "**حدث خطأ اثناء تشغيل التالي .⚡**")

            stream = (
                AudioVideoPiped(file_path, audio_parameters=audio_stream_quality,
                                video_parameters=video_stream_quality)
                if video else AudioPiped(file_path, audio_parameters=audio_stream_quality)
            )

            try:
                await call.change_stream(chat_id, stream)  # type: ignore
            except Exception:
                return await client.send_message(chat_id, "**حدث خطأ اثناء تشغيل التالي .⚡**")

            userx = await client.get_users(user_id)
            if videoid:
                if userx.photo:
                    photo_id = userx.photo.big_file_id
                else:
                    ahmed = await client.get_chat("Elasyoutyy")
                    photo_id = ahmed.photo.big_file_id
                photo = await client.download_media(photo_id)
                img = await gen_thumb(videoid, photo)
            else:
                img = PHOTO

            requester = userx.mention       
            gr = await get_group(bot_username)
            ch = await get_channel(bot_username)
            button = [
                [InlineKeyboardButton(text="END", callback_data=f"stop"), InlineKeyboardButton(text="RESUME", callback_data=f"resume"), InlineKeyboardButton(text="PAUSE", callback_data=f"pause")],
                [InlineKeyboardButton(text="𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🌐", url=f"{ch}"), InlineKeyboardButton(text="𝗚𝗿𝗼𝘂𝗽 ♻️", url=f"{gr}")],
                [InlineKeyboardButton(text=f"{OWNER_NAME}", url="https://t.me/A_q_lp")],
                [InlineKeyboardButton(text="اضف البوت الي مجموعتك او قناتك ⚡", url=f"https://t.me/{bot_username}?startgroup=True")]
            ]
            await message.reply_photo(photo=img, caption=f"**Skipped Streaming **\n\n**Song Name** : {title}\n**Duration Time** {dur}\n**Request By** : {requester}", reply_markup=InlineKeyboardMarkup(button))
            
            try:
                os.remove(file_path)
                os.remove(img)
            except:
                pass

        else:
            await message.reply_text("**خطا في استخدام الأمر**")
    except:
        pass
