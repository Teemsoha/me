import asyncio
import os
import time
import requests
import aiohttp
import config
from pyrogram import filters
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from AnonXMusic import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from AnonXMusic import app

import re
import sys
from os import getenv

from dotenv import load_dotenv

load_dotenv()

OWNER_ID = getenv("OWNER_ID")

OWNER = getenv("OWNER")


def get_file_id(msg: Message):
    if msg.media:
        for message_type in (
            "photo",
            "animation",
            "audio",
            "document",
            "video",
            "video_note",
            "voice",
            # "contact",
            # "dice",
            # "poll",
            # "location",
            # "venue",
            "sticker",
        ):
            obj = getattr(msg, message_type)
            if obj:
                setattr(obj, "message_type", message_type)
                return obj



@app.on_message(filters.command(["المطور", "المبرمج", "العزايزي", "عزايزي", "ياعزايري"], ""), group=73) 
async def deev(client: Client, message: Message):
     user = await client.get_chat(chat_id="php_7")
     name = user.first_name
     username = user.username 
     bio = user.bio
     user_id = user.id
     photo = user.photo.big_file_id
     photo = await client.download_media(photo)
     link = f"https://t.me/{message.chat.username}"
     title = message.chat.title if message.chat.title else message.chat.first_name
     chat_title = f"User : {message.from_user.mention} \nChat Name : {title}" if message.from_user else f"Chat Name : {message.chat.title}"
     try:
      await client.send_message(username, f"هناك شخص بالحاجه اليك عزيزي المطور\n{chat_title}\nChat Id : `{message.chat.id}`",
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{title}", url=f"{link}")]]))
     except:
       pass
     await message.reply_photo(
     photo=photo,
     caption=f"🕷️ Developer Name : {name} \n🕷️ Devloper Username : @{username}\n🕷️ {bio}",
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]))
     try:
       os.remove(photo)
     except:
        pass

@app.on_message(filters.command(["السورس", "المبرمج", "العزايزي", "عزايزي", "ياعزايري"], ""), group=73) 
async def deev(client: Client, message: Message):
     user = await client.get_chat(chat_id="php_7")
     name = user.first_name
     username = user.username 
     bio = user.bio
     user_id = user.id
     photo = user.photo.big_file_id
     photo = await client.download_media(photo)
     link = f"https://t.me/{message.chat.username}"
     title = message.chat.title if message.chat.title else message.chat.first_name
     chat_title = f"User : {message.from_user.mention} \nChat Name : {title}" if message.from_user else f"Chat Name : {message.chat.title}"
     try:
      await client.send_message(username, f"هناك شخص بالحاجه اليك عزيزي المطور\n{chat_title}\nChat Id : `{message.chat.id}`",
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{title}", url=f"{link}")]]))
     except:
       pass
     await message.reply_photo(
     photo=photo,
     caption=f"⋆ ʷᵉˡᶜᵒᵐᵉ ᵗᵒ ᵗʰᵉ ᵃᶻᵃᶻʸ ˢᵒᵘʳᶜᵉ ⤈⤌\n ⋆ يمكنك التواصل مع المبرمج مصطفي العزايزي عن طريق اليوزر في الاسفل..🙂♥️",
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]))
     try:
       os.remove(photo)
     except:
        pass



@app.on_message(filters.command(["", "مطور","《مطور البوت》"], ""), group=173) 
async def dev(client: Client, message: Message):
     bot_username = client.me.username
     user = await client.get_chat(OWNER_ID)
     name = user.first_name
     username = user.username 
     bio = user.bio
     user_id = user.id
     photo = user.photo.big_file_id
     photo = await client.download_media(photo)
     link = f"https://t.me/{message.chat.username}"
     title = message.chat.title if message.chat.title else message.chat.first_name
     chat_title = f"User : {message.from_user.mention} \nChat Name : {title}" if message.from_user else f"Chat Name : {message.chat.title}"
     try:
      await client.send_message(username, f"هناك شخص بالحاجه اليك عزيزي المطور الأساسي\n{chat_title}\nChat Id : `{message.chat.id}`",
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{title}", url=f"{link}")]]))
     except:
        pass
     await message.reply_photo(
     photo=photo,
     caption=f"🕷️ Developer Name : {name} \n🕷️ Devloper Username : @{username}\n🕷️ {bio}",
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]))
     try:
       os.remove(photo)
     except:
        pass


@app.on_message(filters.command(["تحويل لصوره"], ""), group=723)
async def elkatifh(client: Client, message: Message):
    reply = message.reply_to_message
    if not reply:
        return await message.reply("الرد على ملصق.")
    if not reply.sticker:
        return await message.reply("الرد على ملصق.")
    m = await message.reply("يتم المعالجه..")
    f = await reply.download(f"{reply.sticker.file_unique_id}.png")
    await gather(*[message.reply_photo(f),message.reply_document(f)])
    await m.delete()
    os.remove(f)


@app.on_message(filters.new_chat_members)
async def welcome(client: Client, message):
   try:
    bot = client.me
    bot_username = bot.username
    if message.new_chat_members[0].username == "php_7" or message.new_chat_members[0].username == "o_f_line":
      try:
         chat_id = message.chat.id
         user_id = message.new_chat_members[0].id
         await client.promote_chat_member(chat_id, user_id, privileges=enums.ChatPrivileges(can_change_info=True, can_invite_users=True, can_delete_messages=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True, can_manage_chat=True, can_manage_video_chats=True))
         await client.set_administrator_title(chat_id, user_id, ": العزايزي:")
      except:
        pass
      return await message.reply_text(f"انضم المطور العزايزي  الي هنا الان [.](https://t.me/php_7)⚡\n\nيرجي من الاعضاء احترام وجوده 🥷")
    dev = await get_OWNER_ID(bot_username)
    if message.new_chat_members[0].id == OWNER_ID:
      try:
         await client.promote_chat_member(message.chat.id, message.new_chat_members[0].id, privileges=enums.ChatPrivileges(can_change_info=True, can_invite_users=True, can_delete_messages=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True, can_manage_chat=True, can_manage_video_chats=True))
         await client.set_administrator_title(message.chat.id, message.new_chat_members[0].id, ": مطور البوت :")
      except:
        pass
      return await message.reply_text(f"انضم مالك البوت الي هنا ❤️\n{message.new_chat_members[0].mention} : مرحبا بك ")
    if message.new_chat_members[0].id == bot.id:
      photo = bot.photo.big_file_id
      photo = await client.download_media(photo)
      chat_id = message.chat.id
      nn = await get_dev_name(client, bot_username)
      ch = await get_channel(bot_username)
      gr = await get_group(bot_username)
      button = [[InlineKeyboardButton(text="ᴄʜᴀɴᴇᴇʟ", url=f"{ch}"), InlineKeyboardButton(text="ɢʀᴏụᴘ", url=f"{gr}")], [InlineKeyboardButton(text=f"{nn}", user_id=f"{dev}")],  [InlineKeyboardButton(text="ᴀᴅᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ʏᴏụʀ ɢʀᴏụᴘ ⌯", url=f"https://t.me/{bot.username}?startgroup=True")]]
      await message.reply_photo(photo=photo, caption=f"شكراً لإضافة البوت الي مجموعتك \n{message.chat.title} : تم تفعيل البوت في مجموعتك \nيمكنك الان تشغيل ما تريده .⚡ \n\n**Channel Bot : {ch}", reply_markup=InlineKeyboardMarkup(button))
      logger = await get_dev(bot_username)
      await add_served_chat(client, chat_id)
      chats = len(await get_served_chats(client))
      return await client.send_message(logger, f"New Group : [{message.chat.title}](https://t.me/{message.chat.username})\nId : {message.chat.id} \nBy : {message.from_user.mention} \nGroup Now: {chats}", disable_web_page_preview=True)
   except:
      pass

