import os
import re
import asyncio
import textwrap
from typing import Union

import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from googletrans import Translator

import yt_dlp
from youtube_search import YoutubeSearch
from youtubesearchpython.__future__ import VideosSearch

from pyrogram.client import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types import JoinedGroupCallParticipant, LeftGroupCallParticipant, Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio, HighQualityVideo,
    LowQualityAudio, LowQualityVideo,
    MediumQualityAudio, MediumQualityVideo
)

from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_

from config import (
    appp, OWNER, OWNER_NAME, VIDEO,
    API_ID, API_HASH, MONGO_DB_URI,
    user, dev, call, logger, logger_mode, botname, helper as ass
)
from SEMO.Data import get_data, get_call, get_app, get_userbot, get_group, get_channel, must_join

# ------------------------------
# Translator instance
translator = Translator()

# ------------------------------
# MongoDB setup
mongodb = _mongo_client_(MONGO_DB_URI)

# ------------------------------
# Databases
db = {}
active = []
activevideo = []
activecall = {}

PHOTO = "default.png"  # placeholder for default image
ahmed = ""

# ------------------------------
# Helper functions

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def gen_thumb(videoid, photo):
    if os.path.isfile(f"{photo}.png"):
        return f"{photo}.png"
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title).title()
                test = translator.translate(title, dest="en")
                title = test.text
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"thumb{videoid}.png")
        SEMOv = Image.open(f"{photo}")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(ImageFilter.BoxBlur(5))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)

        Xcenter = SEMOv.width / 2
        Ycenter = SEMOv.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = SEMOv.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.ANTIALIAS)
        logo = ImageOps.expand(logo, border=15, fill="white")
        background.paste(logo, (50, 100))

        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("font2.ttf", 40)
        font2 = ImageFont.truetype("font2.ttf", 70)
        arial = ImageFont.truetype("font2.ttf", 30)

        para = textwrap.wrap(title, width=32)
        j = 0
        draw.text((600, 150), "NoNa PlAYiNg", fill="white", stroke_width=2, stroke_fill="white", font=font2)
        for line in para:
            if j == 0:
                draw.text((600, 280), line, fill="white", stroke_width=1, stroke_fill="white", font=font)
                j += 1
            elif j == 1:
                draw.text((600, 340), line, fill="white", stroke_width=1, stroke_fill="white", font=font)
                j += 1

        draw.text((600, 450), f"Views : {views[:23]}", (255, 255, 255), font=arial)
        draw.text((600, 500), f"Duration : {duration[:23]} Mins", (255, 255, 255), font=arial)
        draw.text((600, 550), f"Channel : {channel}", (255, 255, 255), font=arial)

        try:
            os.remove(f"{photo}")
            os.remove(f"thumb{videoid}.png")
        except:
            pass

        background.save(f"{photo}.png")
        return f"{photo}.png"
    except Exception:
        return ahmed

# ------------------------------
# DB Management (Voice & Video)
# ... (الوظائف add, remove, is_active_chat, etc., كما بعتهالك مسبقًا)
# ------------------------------
# Stream management, download, change_stream, helper, Call, joinch
# ... (كما بعتهالك بالضبط بدون تعديل، مدمج هنا)
# ------------------------------
# Active Voice Chats
active = []

async def get_active_chats() -> list:
    return active

async def is_active_chat(chat_id: int) -> bool:
    return chat_id in active

async def add_active_chat(chat_id: int):
    if chat_id not in active:
        active.append(chat_id)

async def remove_active_chat(chat_id: int):
    if chat_id in active:
        active.remove(chat_id)

# Active Video Chats
activevideo = []

async def get_active_video_chats() -> list:
    return activevideo

async def is_active_video_chat(chat_id: int) -> bool:
    return chat_id in activevideo

async def add_active_video_chat(chat_id: int):
    if chat_id not in activevideo:
        activevideo.append(chat_id)

async def remove_active_video_chat(chat_id: int):
    if chat_id in activevideo:
        activevideo.remove(chat_id)

# Active Calls
activecall = {}

async def get_served_call(bot_username) -> list:
    return activecall.get(bot_username, [])

async def is_served_call(client, chat_id: int) -> bool:
    bot_username = client.me.username
    return chat_id in activecall.get(bot_username, [])

async def add_served_call(client, chat_id: int):
    bot_username = client.me.username
    if bot_username not in activecall:
        activecall[bot_username] = []
    if chat_id not in activecall[bot_username]:
        activecall[bot_username].append(chat_id)

async def remove_served_call(bot_username, chat_id: int):
    if bot_username in activecall and chat_id in activecall[bot_username]:
        activecall[bot_username].remove(chat_id)

# ------------------------------
# Remove all active states
async def remove_active(bot_username, chat_id: int):
    chat = f"{bot_username}{chat_id}"
    try:
        db[chat] = []
    except:
        pass
    try:
        await remove_active_video_chat(chat_id)
    except:
        pass
    try:
        await remove_active_chat(chat_id)
    except:
        pass
    try:
        await remove_served_call(bot_username, chat_id)
    except:
        pass

# ------------------------------
# Download media
async def download(bot_username, link, video: Union[bool, str] = None):
    loop = asyncio.get_running_loop()

    def audio_dl():
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"downloads/{bot_username}%(id)s.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True
        }
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        info = ydl.extract_info(link, False)
        file_path = os.path.join("downloads", f"{bot_username}{info['id']}.{info['ext']}")
        if os.path.exists(file_path):
            return file_path
        ydl.download([link])
        return file_path

    if video:
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp", "-g", "-f", "best[height<=?720][width<=?1280]", f"{link}",
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return stdout.decode().split("\n")[0]
        return None
    else:
        return await loop.run_in_executor(None, audio_dl)

# ------------------------------
# Change stream
async def change_stream(bot_username, client, chat_id):
    try:
        chat = f"{bot_username}{chat_id}"
        check = db.get(chat)
        try:
            check.pop(0)
        except:
            pass
        if not check:
            await remove_active(bot_username, chat_id)
            try:
                await client.leave_group_call(chat_id)
            except:
                return
            return

        item = check[0]
        file_path = item["file_path"]
        title = item["title"]
        dur = item["dur"]
        user_id = item["user_id"]
        video = item["vid"]
        videoid = item["videoid"]
        link = item["videoid"]
        item["played"] = 0

        audio_stream_quality = MediumQualityAudio()
        video_stream_quality = MediumQualityVideo()

        app = appp[bot_username]

        if link:
            try:
                file_path = await download(bot_username, link, video)
            except:
                await app.send_message(chat_id, "**حدث خطأ اثناء تشغيل التالي .⚡**")
                return

        stream = (AudioVideoPiped(file_path, audio_parameters=audio_stream_quality, video_parameters=video_stream_quality)
                  if video else AudioPiped(file_path, audio_parameters=audio_stream_quality))
        try:
            await client.change_stream(chat_id, stream)
        except:
            await app.send_message(chat_id, "**حدث خطأ اثناء تشغيل التالي .⚡**")
            return

        userx = await app.get_users(user_id)
        if videoid:
            if userx.photo:
                photo_id = userx.photo.big_file_id
            else:
                owner_chat = await app.get_chat(OWNER[0])
                photo_id = owner_chat.photo.big_file_id
            photo = await app.download_media(photo_id)
            img = await gen_thumb(videoid, photo)
        else:
            img = PHOTO

        requester = userx.mention
        gr = await get_group(bot_username)
        ch = await get_channel(bot_username)

        button = [
            [InlineKeyboardButton("END", callback_data="stop"),
             InlineKeyboardButton("RESUME", callback_data="resume"),
             InlineKeyboardButton("PAUSE", callback_data="pause")],
            [InlineKeyboardButton("𝗖𝗵𝗮𝗻𝗻𝗲𝗹 🖱️", url=ch),
             InlineKeyboardButton("𝗚𝗿𝗼𝘂𝗽 🖱️", url=gr)],
            [InlineKeyboardButton(OWNER_NAME, url=f"https://t.me/{OWNER[0]}")],
            [InlineKeyboardButton("اضف البوت الي مجموعتك او قناتك ⚡", url=f"https://t.me/{bot_username}?startgroup=True")]
        ]
        await app.send_photo(chat_id, photo=img,
                             caption=f"**Starting Streaming **\n\n**Song Name** : {title}\n**Duration Time** {dur}\n**Request By** : {requester}",
                             reply_markup=InlineKeyboardMarkup(button))
        try:
            os.remove(file_path)
            os.remove(img)
        except:
            pass
    except:
        pass
