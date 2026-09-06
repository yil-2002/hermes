import aiohttp
import asyncio
import hmac

def verify_secret(received: str, expected: str) -> bool:
    if not received or not expected: return False
    return hmac.compare_digest(received, expected)

class TelegramClient:
    def __init__(self, token: str):
        self.token = token
        self.api = f"https://api.telegram.org/bot{token}"
        self.session = None
        
    async def init_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def close(self):
        if self.session:
            await self.session.close()

    async def _post(self, method: str, data: dict):
        await self.init_session()
        async with self.session.post(f"{self.api}/{method}", json=data) as resp:
            res = await resp.json()
            if resp.status == 429: # Telegram Retry Storm himoyasi
                ra = res.get("parameters", {}).get("retry_after", 1)
                await asyncio.sleep(ra)
                return await self._post(method, data)
            return res
            
    async def get_file(self, file_id: str):
        return await self._post("getFile", {"file_id": file_id})
        
    async def send_chat_action(self, chat_id: int, action="typing"):
        await self._post("sendChatAction", {"chat_id": chat_id, "action": action})

    async def send_message(self, chat_id: int, text: str, parse_mode="Markdown"):
        limit = 4096
        chunks = [text[i:i+limit] for i in range(0, len(text), limit)]
        for chunk in chunks:
            res = await self._post("sendMessage", {"chat_id": chat_id, "text": chunk, "parse_mode": parse_mode})
            # Markdown buzilgan bo'lsa (unbalanced entities), toza matn sifatida jo'natish (Fallback)
            if not res.get("ok") and "entities" in res.get("description", "").lower():
                await self._post("sendMessage", {"chat_id": chat_id, "text": chunk})
