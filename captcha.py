# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: Concha
# Author: AleksFolt
# Commands:
# .ccaptchaon
# .ccaptchaoff
# ---------------------------------------------------------------------------------

# meta developer: @aleksfolt

import asyncio
import logging
from typing import List

from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class CaptchaMod(loader.Module):
    """Captcha for chats"""

    strings = {
        "name": "Captcha",
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
        self.db = db
        self._client = client
        self.captcha_enabled = False
        self.locked_users: List[dict] = []
        self._client.add_event_handler(self.on_new_member, events.ChatAction)

    async def on_new_member(self, event: events.ChatAction.Event):
        if event.user_added and self.captcha_enabled:
            for user in event.users:
                await self._client.edit_permissions(event.chat_id, user.id, send_messages=False)
                button = [{"text": "Пройти проверку", "callback": self.verify_user, "args": [user.id]}]
                await self.inline.form(
                    text=self.strings["verification_prompt"].format(user.first_name),
                    chat_id=event.chat_id,
                    reply_markup=button,
                )
                self.locked_users.append({"chat_id": event.chat_id, "user_id": user.id})

    async def verify_user(self, call, user_id):
        if call.from_user.id == user_id:
            await self._client.edit_permissions(call.message.chat_id, user_id, send_messages=True)
            await call.answer(self.strings["verification_success"], show_alert=True)
            self.locked_users = [user for user in self.locked_users if user["user_id"] != user_id]

    @loader.unrestricted
    @loader.ratelimit
    async def ccaptchaoncmd(self, message):
        """
        - enable captcha
        """
        self.captcha_enabled = True
        await utils.answer(message, self.strings["captcha_enabled"])

    @loader.unrestricted
    @loader.ratelimit
    async def ccaptchaoffcmd(self, message):
        """
        - disable captcha
        """
        self.captcha_enabled = False
        await utils.answer(message, self.strings["captcha_disabled"])
