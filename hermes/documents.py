import io
import aiohttp
import pypdf
from hermes.config import Config

class DocumentError(Exception):
    pass

async def fetch_and_extract(tg_client, file_id: str, file_name: str, file_size: int) -> str:
    if file_size > Config.MAX_DOC_BYTES:
        raise DocumentError(f"⚠️ Fayl hajmi 20MB dan katta ({file_size} bytes). Telegram limitidan oshib ketdi.")
        
    file_info = await tg_client.get_file(file_id)
    if not file_info.get("ok"):
        raise DocumentError("⚠️ Telegram serveridan fayl ma'lumotlarini olib bo'lmadi.")
        
    file_path = file_info["result"]["file_path"]
    url = f"https://api.telegram.org/file/bot{tg_client.token}/{file_path}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise DocumentError("⚠️ Faylni yuklab olishda xatolik yuz berdi.")
            content = await resp.read()
            
    # Xotira ichida (BytesIO) faylni ishlash - Docker read-only FS xavfsizligi
    if file_name.lower().endswith(".pdf"):
        try:
            reader = pypdf.PdfReader(io.BytesIO(content))
            text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
            return text[:400000] # max chars
        except Exception as e:
            raise DocumentError(f"⚠️ PDF faylini o'qib bo'lmadi: {e}")
    else:
        try:
            text = content.decode("utf-8", errors="replace")
            return text[:400000]
        except Exception as e:
            raise DocumentError(f"⚠️ Matn formatini tahlil qilib bo'lmadi: {e}")
