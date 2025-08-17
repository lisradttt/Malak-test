from pyrogram import filters
from pyrogram.client import Client
from config import OWNER_NAME, GROUP
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from SEMO.Data import get_dev, get_group, get_channel, get_dev_name

# تعريف الكلاينت مرة واحدة
app = Client("bot")

async def safe_get_channel(username):
    return await get_channel(username) or "https://t.me/E_BBC"

async def safe_get_group(username):
    return await get_group(username) or "https://t.me/E_BBC"

async def safe_get_dev(username):
    return await get_dev(username) or 0

async def safe_get_dev_name(client, username):
    return await get_dev_name(client, username) or "Developer"

# ------------------- CALLBACKS -------------------

@app.on_callback_query(filters.regex("arbic"))
async def arbic(client, query: CallbackQuery):
    bot = client.me
    if not bot:
        await query.answer("Bot info not loaded!", show_alert=True)
        return
    username = bot.username or "BotUsername"
    ch = await safe_get_channel(username)
    gr = await safe_get_group(username)
    dev = await safe_get_dev(username)
    devname = await safe_get_dev_name(client, username)

    await query.answer("القائمة الرئيسية")
    await query.edit_message_text(
        f"**{query.from_user.mention} : مرحباً بك عزيزي **\n\n"
        "**انا بوت تشغيل موسيقى صوتية ومرئية .⚡**\n"
        "**قم بإضافة البوت إلي مجموعتك او قناتك .⚡**\n"
        "**سيتم تفعيل البوت وانضمام المساعد تلقائياً**\n"
        "**في حال مواجهت مشاكل انضم هنا **\n**@ **\n"
        "**استخدم الازرار لمعرفه اوامر الاستخدام .⚡ **",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("اضف البوت اللي مجموعتك.", url=f"https://t.me/{username}?startgroup=true")],
                [InlineKeyboardButton("zombie", url="https://t.me/Zo_Mbi_e")],
                [InlineKeyboardButton("طريقة التشغيل .", callback_data="bcmds"),
                 InlineKeyboardButton("طريقة التفعيل.", callback_data="bhowtouse")],
                [InlineKeyboardButton("جروب البوت.", url=gr),
                 InlineKeyboardButton("قناه التحديثات.", url=ch)],
                [InlineKeyboardButton(devname, user_id=int(dev))],
            ]
        ),
        disable_web_page_preview=True,
    )

@app.on_callback_query(filters.regex("english"))
async def english(client, query: CallbackQuery):
    bot = client.me
    if not bot:
        await query.answer("Bot info not loaded!", show_alert=True)
        return
    username = bot.username or "BotUsername"
    ch = await safe_get_channel(username)
    gr = await safe_get_group(username)
    dev = await safe_get_dev(username)
    devname = await safe_get_dev_name(client, username)

    await query.answer("Home Start")
    await query.edit_message_text(
        f"""A Telegram Music Bot
Played Music and Video in VC
Bot Online Now 
Add Me To Your Chat
Powered By [{OWNER_NAME}]""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Add me to your Group", url=f"https://t.me/{username}?startgroup=true")],
                [InlineKeyboardButton("Donate", url="https://t.me/Zo_Mbi_e")],
                [InlineKeyboardButton("Commands", callback_data="cbcmds"),
                 InlineKeyboardButton("Basic Guide", callback_data="cbhowtouse")],
                [InlineKeyboardButton("Group", url=gr),
                 InlineKeyboardButton("Channel", url=ch)],
                [InlineKeyboardButton(devname, user_id=int(dev))],
            ]
        ),
        disable_web_page_preview=True,
    )

@app.on_callback_query(filters.regex("cbhowtouse"))
async def cbhowtouse(_, query: CallbackQuery):
    await query.answer("user guide")
    await query.edit_message_text(
        f"""❓ **Basic Guide for using this bot:**
1.) **First, add me to your group.**
2.) **Then, promote me as administrator and give all permissions except Anonymous Admin.**
3.) **After promoting me, type /reload in group to refresh the admin data.**
3.) **Add Assistant to your group or invite her.**
4.) **Turn on the video chat first before start to play video/music.**
5.) **Sometimes, reloading the bot by using /reload command can help you to fix some problem.**
📌 **If the userbot not joined to video chat, make sure if the video chat already turned on.**
💡 **If you have a follow-up questions about this bot, you can tell it on my support chat here: @Zo_Mbi_e**
⚡ __ Developer by [{OWNER_NAME}]""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="english")]]
        ),
    )

@app.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(_, query: CallbackQuery):
    await query.answer("commands menu")
    await query.edit_message_text(
        f"""✨ **Hello [{query.message.from_user.first_name}](tg://user?id={query.message.from_user.id}) !**
» **press the button below to read the explanation and see the list of available commands !**
⚡ __Powered by [{OWNER_NAME}] A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Admin Cmd", callback_data="cbadmin"),
                 InlineKeyboardButton("Bisc Cmd", callback_data="cbbasic")],
                [InlineKeyboardButton("Sudo Cmd", callback_data="cbsudo")],
                [InlineKeyboardButton("Go Back", callback_data="english")],
            ]
        ),
    )

# باقي الدوال cbbasic, cbadmin, cbsudo, bhowtouse, bcmds... كما هي بدون حذف
