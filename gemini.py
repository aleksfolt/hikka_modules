import os
import google.generativeai as genai
from .. import loader, utils
from ..inline.types import InlineQuery, InlineCall

@loader.tds
class GeminiAPIMod(loader.Module):
    """GeminiAPI"""

    strings = {
        "name": "GeminiAPI",
        "no_key": "<emoji document_id=5843952899184398024>🚫</emoji> API ключ не найден",
        "error": "<emoji document_id=5462882007451185227>🚫</emoji> Произошла ошибка при запросе",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "gemini_api_key",
                None,
                lambda: "Введите ваш API ключ от Gemini",
                validator=loader.validators.Hidden(),
            )
        )
        self.chat_sessions = {}

    def configure_genai(self):
        api_key = self.config["gemini_api_key"]
        if api_key is None:
            return False
        genai.configure(api_key=api_key)
        return True

    def get_or_create_session(self, user_id):
        if user_id not in self.chat_sessions:
            self.chat_sessions[user_id] = {
                "history": [],
                "model": genai.GenerativeModel(
                    model_name="gemini-1.5-pro",
                    generation_config={
                        "temperature": 1,
                        "top_p": 0.95,
                        "top_k": 64,
                        "max_output_tokens": 8192,
                        "response_mime_type": "text/plain",
                    }
                )
            }
        return self.chat_sessions[user_id]

    @loader.inline_everyone
    async def gemini_inline_handler(self, query: InlineQuery):
        """Handle inline query with Gemini API"""
        if not self.configure_genai():
            await query.edit(self.strings("no_key"))
            return

        user_id = query.from_user.id
        session = self.get_or_create_session(user_id)
        chat_session = session["model"].start_chat(history=session["history"])

        try:
            response = chat_session.send_message(query.query)
            result_text = response.text

            # Update history
            session["history"].append({"role": "user", "content": query.query})
            session["history"].append({"role": "system", "content": result_text})
        except Exception as e:
            await query.edit(self.strings("error"))
            return

        return {
            "title": "Gemini Response",
            "thumb": "https://te.legra.ph/file/7772a7dae6290f0a612a6.png",
            "description": "Generated response from Gemini API",
            "message": f"<i>{result_text}</i>",
        }

    async def cleardialogcmd(self, message):
        """Clear the dialogue history for the user"""
        user_id = message.from_id
        if user_id in self.chat_sessions:
            del self.chat_sessions[user_id]
        await utils.answer(message, "Dialogue history cleared.")
