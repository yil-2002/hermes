# Hermes

Umumiy routing qoidalari (S/A/B/C, `dirijyor:scout` / `dirijyor:builder` / `dirijyor:bulk-worker`)
`dirijyor` plugin'idan keladi: https://github.com/yil-2002/dirijyor — bu yerda faqat loyihaga xos ma'lumot.

## Loyiha
Telegram orqali ishlaydigan AI agent (J.A.R.V.I.S. persona), aiohttp asosida.

- `server.py` — aiohttp server: Telegram webhook + Mini App sahifasi
- `hermes/orchestrator.py` — so'rovni qayta ishlash, byudjet tekshiruvi, MoE tier routing (LLM chaqiruvi hali simulyatsiya)
- `hermes/config.py` — barcha sozlamalar env o'zgaruvchilardan (`.env.example` ga qarang)
- `hermes/memory.py` — SQLite (`memory.db`): xotira va token xarajati ledger'i
- `hermes/telegram.py`, `hermes/documents.py`, `voice.py` — Telegram API, hujjat o'qish (pypdf), ovoz (edge-tts)
- `prompts/HERMES_CORE_SYSTEM.md` — asosiy system prompt
- `deploy/nginx-hermes.conf` — nginx konfiguratsiyasi

## Tekshirish
- `python -m py_compile <fayl>`
- testlar qo'shilsa: `pytest` (pytest-asyncio o'rnatilgan)

## Maxfiy
`.env`, `memory.db` — hech qachon o'qilmaydi, commit qilinmaydi va DeepSeek'ga yuborilmaydi.
