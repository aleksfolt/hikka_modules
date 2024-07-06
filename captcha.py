# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the Copyleft license.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: captcha
# Author: AleksFolt
# Commands:
# .ccaptchaon
# .ccaptchaoff
# ---------------------------------------------------------------------------------

"""
                                _             
  __   _____  ___  ___ ___   __| | ___ _ __   
  \ \ / / __|/ _ \/ __/ _ \ / _` |/ _ \ '__|  
   \ V /\__ \  __/ (_| (_) | (_| |  __/ |     
    \_/ |___/\___|\___\___/ \__,_|\___|_|     

    Copyleft 2024 t.me/aleksfolt                                                            
    This program is free software; you can redistribute it and/or modify 

"""
# meta developer: @aleksfolt
# meta pic: https://img.icons8.com/color/344/captcha.png
# meta banner: https://chojuu.vercel.app/api/banner?img=https://img.icons8.com/color/344/captcha.png&title=Captcha&description=Module%20for%20inline%20captcha

__version__ = (1, 0, 0)

import logging

from telethon import TelegramClient, events

from .. import loader  # type: ignore
from ..inline.types import InlineCall  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class CaptchaMod(loader.Module):
    """Module for inline captcha"""

    strings = {
        "name": "🛡 Captcha",
        "captcha_enabled": "🔐 <b>Captcha enabled. New members will be muted until verification.</b>",
        "captcha_disabled": "🔓 <b>Captcha disabled. New members will not be muted.</b>",
        "verification_prompt": "🔒 <b>Welcome, {0}! Please verify by clicking the button below:</b>",
        "verification_success": "✅ <b>Verification successful!</b>",
    }

    strings_ru = {
        "captcha_enabled": "🔐 <b>Каптча включена. Новые участники будут мутированы до прохождения проверки.</b>",
        "captcha_disabled": "🔓 <b>Каптча отключена. Новые участники больше не будут мутированы.</b>",
        "verification_prompt": "🔒 <b>Добро пожаловать, {0}! Пожалуйста, пройдите проверку, нажав на кнопку ниже:</b>",
        "verification_success": "✅ <b>Вы успешно прошли проверку!</b>",
    }

    async def client_ready(self, client: TelegramClient, db):
        self._db = db
        self._client = client
        self.captcha_enabled = False
        self._client.add_event_handler(self.on_new_member, events.ChatAction())

    async def on_new_member(self, event):
        if event.user_added and self.captcha_enabled:
            for user in event.users:
                await self._client.edit_permissions(event.chat_id, user.id, send_messages=False)
                button = [{"text": "Пройти проверку", "callback": self.verify_user, "args": [user.id]}]
                await self.inline.form(
                    text=self.strings["verification_prompt"].format(user.first_name),
                    chat_id=event.chat_id,
                    reply_markup=button,
                )

    async def verify_user(self, call: InlineCall, user_id):
        if call.from_user.id == user_id:
            await self._client.edit_permissions(call.message.chat_id, user_id, send_messages=True)
            await call.answer(self.strings["verification_success"], show_alert=True)

    @loader.unrestricted
    @loader.ratelimit
    async def ccaptchaoncmd(self, message):
        """
        - enable captcha
        """
        self.captcha_enabled = True
        await message.reply(self.strings["captcha_enabled"])

    @loader.unrestricted
    @loader.ratelimit
    async def ccaptchaoffcmd(self, message):
        """
        - disable captcha
        """
        self.captcha_enabled = False
        await message.reply(self.strings["captcha_disabled"])
