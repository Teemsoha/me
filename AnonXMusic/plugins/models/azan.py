from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.types import InlineKeyboardMarkup as Markup, InlineKeyboardButton as Button
from AnonXMusic import app
from datetime import datetime
import requests
from AnonXMusic.core.call import Anony
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from AnonXMusic.utils.database import *
from pytgcalls.exceptions import NoActiveGroupCall, TelegramServerError, AlreadyJoinedError
from asyncio import create_task, sleep
from AnonXMusic.core.mongo import mongodb
from AnonXMusic.misc import SUDOERS
from pyrogram.enums import ParseMode

db = mongodb[f"azan{app.me.id}"]

async def add(chat_id, _timezone):
    document = {"chat_id": chat_id, "timezone": _timezone}
    await db.insert_one(document)

async def delete(chat_id):
    query = {"chat_id": chat_id}
    await db.delete_one(query)

async def exists(chat_id):
    query = {"chat_id": chat_id}
    return await db.count_documents(query) > 0

async def get_timezone(chat_id):
    query = {"chat_id": chat_id}
    document = await db.find_one(query)
    return document["timezone"]

async def all():
    documents = db.find()
    docs = await documents.to_list(length=1)
    _all = []
    while docs:
        _all.append(docs[0])
        docs = await documents.to_list(length=1)
    return _all


timezonesMarkup = Markup([
    [
        Button("- القاهرة (مصر) -", callback_data="timezone Africa/Cairo"),
        Button("- بغداد (العراق) -", callback_data="timezone Asia/Baghdad"),
        Button("- دمشق (سوريا) -", callback_data="timezone Asia/Damascus")
    ],
    [
        Button("- الكويت -", callback_data="timezone Asia/Kuwait"), 
        Button("- بيروت (لبنان) -", callback_data="timezone Asia/Beirut"),
        Button("- صنعاء (اليمن) -", callback_data="timezone Asia/Sana'a")
    ],
    [
        Button("- الرياض (المملكه العربيه السعوديه) -", callback_data="timezone Asia/Riyadh")
    ]
])


@app.on_message(filters.command("تفعيل الاذان", "") & ~filters.private)
async def adhanActivition(_: Client, message: Message):
    chat_id = message.chat.id
    if not await exists(chat_id):
        await message.reply("- اختر المنطقه الزمنيه لهذه المجموعه من فضلك 🦋❤️.\n√", reply_markup=timezonesMarkup)
    else: await message.reply("الأذان مفعل هنا من قبل 🦋❤️.")


@app.on_callback_query(filters.regex(r"^(timezone )"))
async def activition(_: Client, callback: CallbackQuery):
    _timezone = callback.data.split()[1]
    chat_id = callback.message.chat.id
    await add(chat_id, _timezone)
    create_task(adhan(chat_id, _timezone))
    await callback.message.edit_text(f"- تم تفعيل الأذان 🦋❤️.\n- المنطقه الزمنيه : {_timezone}\n- المدينه : {_timezone.split('/')[1]}")


@app.on_message(filters.command("تعطيل الاذان", "") & ~filters.private)
async def adhanDeactivate(_: Client, message: Message):
    chat_id = message.chat.id
    if not await exists(chat_id):
        await message.reply("الأذان غير مفعل بالفعل 💔.", reply_to_message_id=message.id)
    else:
        await delete(chat_id)
        await message.reply("تم إلغاء تفعيل الأذان 💔.")


@app.on_message(filters.command("الاذان", "") & SUDOERS)
async def activated(_: Client, message: Message):
    chats, id = await all(), 1
    caption = "- الأذان مفعل في المجموعات التاليه: \n\n" if len(chats) else False
    if not caption: return await message.reply("- لم يتم تفعيل الأذان بواسطة أي دردشه.")
    for chat in chats:
        ichat = await app.get_chat(chat["chat_id"])
        if ichat.username is None: caption += f"{id}- {ichat.title} -> ({chat['chat_id']}) (دردشه خاصه)\n"; id+=1; continue
        caption += f"{id}- [{ichat.title}](https://t.me/{ichat.username}) -> ({chat['chat_id']})\n"; id+=1
    await message.reply(caption, reply_to_message_id = message.id, parse_mode=ParseMode.MARKDOWN)
    
    
async def calls_stop(chat_id):
    await Anony.force_stop_stream(chat_id)


async def play(chat_id):
    assistant = await group_assistant(Anony, chat_id)
    audio = "./AnonXMusic/assets/azan.m4a"
    stream = AudioPiped(audio)
    try:await assistant.join_group_call(
            chat_id,
            stream,
            stream_type=StreamType().pulse_stream,
        )
    except NoActiveGroupCall:
        try:
            await Anony.join_assistant(chat_id, chat_id)
        except Exception as e:
            await app.send_message(chat_id, f"خطأ: {e}")
    except TelegramServerError:
        await app.send_message(chat_id, "عذرًا، هناك مشكلات في سيرفر التليجرام")
    except AlreadyJoinedError:
        await calls_stop(chat_id)
        try:
            await assistant.join_group_call(
                chat_id,
                stream,
                stream_type=StreamType().pulse_stream,
            )
        except Exception as e:
            await app.send_message(chat_id, f"خطأ: {e}")


pnames: dict = {
    'Fajr': "الفجر", 
    'Sunrise': "الشروق", 
    'Dhuhr': "الظهر", 
    'Asr': "العصر",
    'Maghrib': "المغرب", 
    'Isha': "العشاء", 
}


def prayers(city):
    method: int = 1
    params = {
        "address" : city,
        "method" : method, 
        "school" : 0
    }
    res = requests.get("http://api.aladhan.com/timingsByAddress", params=params)
    data = res.json()
    timings = data["data"]["timings"]
    del timings["Sunrise"]; del timings["Sunset"]; del timings["Imsak"]; del timings["Midnight"]; del timings["Firstthird"]; del timings["Lastthird"]
    return timings


async def adhan(chat_id, _timezone):
    while await exists(chat_id):
        current_time = datetime.now(timezone(_timezone)).strftime("%H:%M")
        try:prayers_time = prayers(_timezone.split("/")[1].lower())
        except requests.exceptions.ConnectionError:continue
        if current_time in list(prayers_time.values()):
            pname = pnames[
                list(prayers_time.items())[list(prayers_time.values()).index(current_time)][0]
            ]
        else:
            await sleep(10)
            continue
        await calls_stop(chat_id)
        a = await app.send_message(chat_id, f"حان الآن وقت أذان {pname} 🦋❤️\nجارٍ تشغيل الأذان...")
        await play(chat_id)
        await sleep(173)
        await calls_stop(chat_id)
        await a.edit_text("انتهى الأذان 🦋❤️.")


async def reactive():
    chats = await all()
    for chat in chats:
        create_task(adhan(chat["chat_id"], chat["timezone"]))
        
create_task(reactive())

# 𝗪𝗥𝗜𝗧𝗧𝗘𝗡 𝗕𝗬 : @BENN_DEV
# 𝗦𝗢𝗨𝗥𝗖𝗘 : @BENfiles
# متبقاش حرامي وخماط ياحرامي ✨️
