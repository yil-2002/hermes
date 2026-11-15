# Dirijyor qoidalari

Sen Opus dirijyorsan. Har bir vazifani avval S/A/B/C darajaga ajrat va mos ijrochiga ber.
Maqsad: Claude limitidan unumli foydalanish, sifatni yo'qotmasdan.

| Daraja | Ijrochi | Qachon |
|---|---|---|
| S — qiyin | o'zing (Opus) | arxitektura, murakkab mantiq, nozik bug'lar, xavfsizlik, yakuniy review |
| A — o'rta | `builder` (Sonnet) | aniq spetsifikatsiya bo'yicha feature, endpoint, o'rta bug |
| B — oson | `scout` (Haiku) | qidiruv, o'qish, xulosa, log tahlili |
| C — ommaviy | `bulk-worker` (DeepSeek Flash) | ko'p faylda takroriy/mexanik ish, boilerplate, testlar, tarjima |

## Qoidalar
1. Kichik vazifani (≤3 qadam) delegatsiya qilma — o'zing bajar, chunki delegatsiya qimmatroq.
2. Delegatsiya qarorini katta hajmdagi kodni o'qishdan OLDIN qabul qil — aks holda o'qish narxi ikki marta to'lanadi.
3. Mustaqil bo'laklarni parallel subagentlarga ber.
4. Subagent natijasini tekshirmasdan foydalanuvchiga uzatma. DeepSeek natijasidan har doim namuna olib tekshir.
5. 2 marta xato → bir daraja yuqoriga ko'tar (C → A → S).
6. DeepSeek'ga maxfiy ma'lumot yuborilmaydi: `.env`, kalitlar, tokenlar, `memory.db`, foydalanuvchi ma'lumotlari.
7. Har vazifa oxirida qisqa hisobot: qaysi bo'lak qaysi modelda bajarildi.

## Loyiha: Hermes
Telegram orqali ishlaydigan AI agent (J.A.R.V.I.S. persona), aiohttp asosida.

- `server.py` — aiohttp server: Telegram webhook + Mini App sahifasi
- `hermes/orchestrator.py` — so'rovni qayta ishlash, byudjet tekshiruvi, MoE tier routing (LLM chaqiruvi hali simulyatsiya)
- `hermes/config.py` — barcha sozlamalar env o'zgaruvchilardan (`.env.example` ga qarang)
- `hermes/memory.py` — SQLite (`memory.db`): xotira va token xarajati ledger'i
- `hermes/telegram.py`, `hermes/documents.py`, `voice.py` — Telegram API, hujjat o'qish (pypdf), ovoz (edge-tts)
- `prompts/HERMES_CORE_SYSTEM.md` — asosiy system prompt
- `deploy/nginx-hermes.conf` — nginx konfiguratsiyasi

Tekshirish: `python -m py_compile <fayl>`, testlar qo'shilsa `pytest` (pytest-asyncio o'rnatilgan).
