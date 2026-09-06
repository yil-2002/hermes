import asyncio
import logging
from collections import OrderedDict
from aiohttp import web
from hermes.config import Config
from hermes.telegram import TelegramClient, verify_secret
from hermes.memory import MemoryStore
from hermes.orchestrator import HermesOrchestrator
from hermes.documents import fetch_and_extract, DocumentError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hermes.server")

# Deduplication uchun LRU kesh (10,000 ta update_id)
PROCESSED_UPDATES = OrderedDict()

async def keep_typing(tg_client, chat_id, stop_event):
    """Tier 2/3 LLM o'ylayotganda Telegram typing uzilib qolmasligi uchun Heartbeat"""
    while not stop_event.is_set():
        await tg_client.send_chat_action(chat_id, "typing")
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=4.5)
        except asyncio.TimeoutError:
            pass

async def background_agent_run(app, chat_id, text, image_urls, doc_text):
    """Fast-ACK'dan so'ng orqa fonda ishlovchi jarayon"""
    tg_client = app["tg"]
    orchestrator = app["orchestrator"]
    stop_event = asyncio.Event()
    
    typing_task = asyncio.create_task(keep_typing(tg_client, chat_id, stop_event))
    
    try:
        res_text = await orchestrator.handle(
            message=text, 
            session_id=f"tg_{chat_id}", 
            image_urls=image_urls,
            document_text=doc_text
        )
    except Exception as e:
        res_text = f"Tizim xatosi yuz berdi: {e}"
    finally:
        stop_event.set()
        await typing_task
        
    await tg_client.send_message(chat_id, res_text)

async def telegram_webhook(request: web.Request) -> web.Response:
    # 1. Secret Token himoyasi (Xarajat va SSRF himoyasi)
    secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if not verify_secret(secret, Config.WEBHOOK_SECRET):
        return web.Response(status=403, text="Forbidden")

    data = await request.json()
    update_id = data.get("update_id")
    
    # 2. Dedup (Takroriy so'rovlarni filtrlash)
    if update_id in PROCESSED_UPDATES:
        return web.Response(status=200)
    PROCESSED_UPDATES[update_id] = True
    if len(PROCESSED_UPDATES) > 10000:
        PROCESSED_UPDATES.popitem(last=False)

    message = data.get("message")
    if not message:
        return web.Response(status=200)

    chat_id = message["chat"]["id"]
    user_id = message["from"]["id"]

    # 3. Zero-Cost Whitelist Guard
    if Config.ALLOWED_USERS and user_id not in Config.ALLOWED_USERS:
        return web.Response(status=200)

    text = message.get("text") or message.get("caption") or ""
    doc_text = None
    image_urls = []
    
    tg_client = request.app["tg"]

    # 4. Hujjat (Document) tahlili
    if "document" in message:
        doc = message["document"]
        try:
            doc_text = await fetch_and_extract(tg_client, doc["file_id"], doc.get("file_name", ""), doc.get("file_size", 0))
        except DocumentError as e:
            await tg_client.send_message(chat_id, str(e))
            return web.Response(status=200)

    # 5. Tasvir (Vision) tahlili
    if "photo" in message and message["photo"]:
        photo = message["photo"][-1]
        file_info = await tg_client.get_file(photo["file_id"])
        if file_info.get("ok"):
            fp = file_info["result"]["file_path"]
            image_urls.append(f"https://api.telegram.org/file/bot{tg_client.token}/{fp}")

    if not text and not doc_text and not image_urls:
        return web.Response(status=200)

    # 6. Orqa fonda ishga tushirish va darhol 200 Fast-ACK berish
    task = asyncio.create_task(background_agent_run(request.app, chat_id, text, image_urls, doc_text))
    request.app["active_tasks"].add(task)
    task.add_done_callback(request.app["active_tasks"].discard)

    return web.Response(status=200)

async def on_startup(app):
    app["tg"] = TelegramClient(Config.BOT_TOKEN)
    app["db"] = MemoryStore(Config.DB_PATH)
    app["orchestrator"] = HermesOrchestrator(app["db"])
    app["active_tasks"] = set()

async def on_shutdown(app):
    # Graceful shutdown: In-flight javoblarni yo'qotmaslik uchun 12 soniya kutish
    if app["active_tasks"]:
        await asyncio.wait(app["active_tasks"], timeout=12.0)
    await app["tg"].close()

app = web.Application()
app.router.add_post("/webhook/telegram", telegram_webhook)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    web.run_app(app, host="127.0.0.1", port=8080)
