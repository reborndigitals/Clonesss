from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import SUPPORT_CHAT


def botplaylist_markup(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_9"], url=SUPPORT_CHAT),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
        [
            InlineKeyboardButton(
                text="ɴᴇᴛᴡᴏʀᴋ", url=f"https://t.me/HeartBeat_Offi",
            ),
            InlineKeyboardButton(
                text="ᴄʜᴀᴛ", url=f"https://t.me/HeartBeat_Fam",
            )
        ],
    ]
    return buttons


def close_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
            [
            InlineKeyboardButton(
                text="ɴᴇᴛᴡᴏʀᴋ", url=f"https://t.me/HeartBeat_Offi",
            ),
            InlineKeyboardButton(
                text="ᴄʜᴀᴛ", url=f"https://t.me/HeartBeat_Fam",
            )
            ],
        ]
    )
    return upl


def supp_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["S_B_9"],
                    url=SUPPORT_CHAT,
                ),
            ],
            [
            InlineKeyboardButton(
                text="ɴᴇᴛᴡᴏʀᴋ", url=f"https://t.me/HeartBeat_Offi",
            ),
            InlineKeyboardButton(
                text="ᴄʜᴀᴛ", url=f"https://t.me/HeartBeat_Fam",
            )
            ],
        ]
    )
    return upl
