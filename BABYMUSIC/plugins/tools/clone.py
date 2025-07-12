import re
import logging
import asyncio
import importlib
from sys import argv
from pyrogram import idle
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import (
    AccessTokenExpired,
    AccessTokenInvalid,
)
from BABYMUSIC.utils.database import get_assistant
from config import API_ID, API_HASH
from BABYMUSIC import app
from BABYMUSIC.misc import SUDOERS
from BABYMUSIC.utils.database import get_assistant, clonebotdb
from config import LOGGER_ID

CLONES = set()


@app.on_message(filters.command("clone"))
async def clone_txt(client, message):
    userbot = await get_assistant(message.chat.id)
    if len(message.command) > 1:
        bot_token = message.text.split("/clone", 1)[1].strip()
        mi = await message.reply_text("Please wait while I process the bot token.")
        try:
            ai = Client(
                bot_token,
                API_ID,
                API_HASH,
                bot_token=bot_token,
                plugins=dict(root="BABYMUSIC.cplugin"),
            )
            await ai.start()
            bot = await ai.get_me()
            bot_users = await ai.get_users(bot.username)
            bot_id = bot_users.id

        except (AccessTokenExpired, AccessTokenInvalid):
            await mi.edit_text(
                "You have provided an invalid bot token. Please provide a valid bot token."
            )
            return
        except Exception as e:
            await mi.edit_text(f"An error occurred: {str(e)}")
            return

        # Proceed with the cloning process
        await mi.edit_text(
            "Cloning process started. Please wait for the bot to be start."
        )
        try:

            await app.send_message(
                LOGGER_ID, f"**#New_Clones**\n\n**Bot:- @{bot.username}**"
            )
            await userbot.send_message(bot.username, "/start")

            details = {
                "bot_id": bot.id,
                "is_bot": True,
                "user_id": message.from_user.id,
                "name": bot.first_name,
                "token": bot_token,
                "username": bot.username,
            }
            clonebotdb.insert_one(details)
            CLONES.add(bot.id)
            await mi.edit_text(
                f"Bot @{bot.username} has been successfully cloned and started ✅.\n**Remove cloned by :- /delclone \n\n 𝗝𝗼𝗶𝗻: @HeartBeat_Fam **"
            )
        except BaseException as e:
            logging.exception("Error while cloning bot. 𝐉𝐨𝐢𝐧: @HeartBeat_Fam")
            await mi.edit_text(
                f"⚠️ <b>ᴇʀʀᴏʀ:</b>\n\n<code>{e}</code>\n\n**ᴋɪɴᴅʟʏ ғᴏᴡᴀʀᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ @HeartBeat_Fam admins ᴛᴏ ɢᴇᴛ ᴀssɪsᴛᴀɴᴄᴇ**"
            )
    else:
        await message.reply_text(
            "**Give Bot Token After /clone Command From @Botfather.**"
        )


@app.on_message(
    filters.command(
        [
            "deletecloned",
            "delcloned",
            "delclone",
            "deleteclone",
            "removeclone",
            "cancelclone",
        ]
    )
)
async def delete_cloned_bot(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text(
                "**⚠️ Please provide the bot token after the command.**"
            )
            return

        bot_token = " ".join(message.command[1:])
        await message.reply_text("Processing the bot token...")

        cloned_bot = clonebotdb.find_one({"token": bot_token})
        if cloned_bot:
            clonebotdb.delete_one({"token": bot_token})
            CLONES.remove(cloned_bot["bot_id"])
            await message.reply_text(
                "**🤖 your cloned bot has been disconnected from my server ☠️\nClone by :- /clone \n\n 𝗝𝗼𝗶𝗻: @HeartBeat_Fam **"
            )
        else:
            await message.reply_text(
                "**⚠️ The provided bot token is not in the cloned list.**"
            )
    except Exception as e:
        await message.reply_text("An error occurred while deleting the cloned bot. \n 𝗝𝗼𝗶𝗻: @HeartBeat_Fam ")
        logging.exception(e)


async def restart_bots():
    global CLONES
    try:
        logging.info("Restarting all cloned bots........")
        bots = clonebotdb.find()
        for bot in bots:
            bot_token = bot["token"]
            ai = Client(
                f"{bot_token}",
                API_ID,
                API_HASH,
                bot_token=bot_token,
                plugins=dict(root="BABYMUSIC.cplugin"),
            )
            await ai.start()
            bot = await ai.get_me()
            if bot.id not in CLONES:
                try:
                    CLONES.add(bot.id)
                except Exception:
                    pass
    except Exception as e:
        logging.exception("Error while restarting bots.")


@app.on_message(filters.command("cloned") & SUDOERS)
async def list_cloned_bots(client, message):
    try:
        cloned_bots = clonebotdb.find()
        cloned_bots_list = await cloned_bots.to_list(length=None)

        if not cloned_bots_list:
            await message.reply_text("No bots have been cloned yet.")
            return

        total_clones = len(cloned_bots_list)
        text = f"Total Cloned Bots: {total_clones}\n\n"

        for bot in cloned_bots_list:
            text += f"Bot ID: {bot['bot_id']}\n"
            text += f"Bot Name: {bot['name']}\n"
            text += f"Bot Username: @{bot['username']}\n\n"

        await message.reply_text(text)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("An error occurred while listing cloned bots.")

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@app.on_message(filters.command("delallclone") & SUDOERS)
async def delete_all_clones(client, message):
    if message.from_user.id not in SUDOERS:
        await message.reply_text("❌ You are not authorized to use this command.")
        return
    confirmation_msg = await message.reply_text(
        "⚠️ **Are you sure you want to delete all cloned bots? This action cannot be undone.**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("✅ YES", callback_data="confirm_delete"),
                    InlineKeyboardButton("❌ NO", callback_data="cancel_delete"),
                ]
            ]
        ),
    )

    try:
        @app.on_callback_query(filters.user(message.from_user.id))
        async def handle_callback_query(client, callback_query):
            if callback_query.message.id != confirmation_msg.id:
                return

            if callback_query.data == "confirm_delete":
                deleted_count = clonebotdb.delete_many({}).deleted_count
                CLONES.clear()
                await callback_query.message.edit_text(
                    f"✅ Successfully deleted all {deleted_count} cloned bots from the database."
                )
                await client.send_message(
                    LOGGER_ID,
                    f"**#Clones_Deleted**\n\nAll {deleted_count} cloned bots have been deleted by {message.from_user.mention}.",
                )
            elif callback_query.data == "cancel_delete":
                await callback_query.message.edit_text("❌ Action canceled. No bots were deleted.")
            await callback_query.answer()

        await asyncio.sleep(30)
        await confirmation_msg.edit_text("❌ Timeout. No bots were deleted.", reply_markup=None)
    except Exception as e:
        logging.exception(e)
        await message.reply_text("❌ An error occurred while processing your request.")
