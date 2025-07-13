from pyrogram.types import InlineKeyboardButton

import config
from BABYMUSIC import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
        ],
        [
            InlineKeyboardButton(text="▪️ʜᴇʟᴘ▪️", callback_data="settings_back_helper"),
            InlineKeyboardButton(text="▪️sᴇᴛ▪️", callback_data="settings_helper"),
        ],
        [
            InlineKeyboardButton(text="▪️sᴜᴘᴘᴏʀᴛ▪️", url=config.CHAT),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="⛩️ ᴧᴅᴅ мᴇ ʙᴧʙʏ ⛩️",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text="▪️sᴜᴘᴘᴏꝛᴛ▪️", url=config.SUPPORT_CHAT),
            InlineKeyboardButton(text="▪️ᴜᴘᴅᴀᴛᴇ▪️", url=config.SUPPORT_CHANNEL),    
        ],
        [
            InlineKeyboardButton(
                text="🏩 ʜᴇʟᴘ ᴧиᴅ ᴄᴏᴍᴍᴧɴᴅs 🏩", callback_data="settings_back_helper"
            )
        ],
    ]
    return buttons
