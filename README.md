# Hermes

Telegram orqali ishlaydigan AI agent (J.A.R.V.I.S.). Ishlab chiqish Claude Code'dagi **multi-agent dirijyor** tizimi bilan olib boriladi.

---

# 🎼 Multi-Agent Dirijyor

Claude Code uchun ko'p modelli agent tizimi. **Opus** dirijyor bo'lib ishlaydi: vazifani qiyinlik darajasiga qarab bo'laklarga ajratadi va har bir bo'lakni mos modelga yo'naltiradi. Maqsad: Claude limitlaridan unumli foydalanish, sifatni yo'qotmasdan.

```
                    ┌──────────────────────┐
     Foydalanuvchi ─▶│  Opus (dirijyor)     │◀─ yakuniy tekshiruv
                    └──────────┬───────────┘
          ┌────────────────────┼─────────────────────┐
          ▼                    ▼                     ▼
  ┌───────────────┐   ┌────────────────┐   ┌──────────────────────┐
  │ Sonnet        │   │ Haiku          │   │ DeepSeek Flash       │
  │ o'rta ishlar  │   │ qidiruv, oson  │   │ ommaviy / mexanik    │
  │ (Claude limit)│   │ (Claude limit) │   │ (limitdan TASHQARI)  │
  └───────────────┘   └────────────────┘   └──────────────────────┘
```

## 📐 Routing qoidalari

| Daraja | Model | Agent | Qanday vazifalar |
|---|---|---|---|
| **S — qiyin** | Opus | — (dirijyorning o'zi) | Arxitektura, murakkab mantiq, nozik bug'lar, xavfsizlik, yakuniy review |
| **A — o'rta** | Sonnet | `builder` | Oddiy feature, aniq spetsifikatsiya bo'yicha kod, o'rta bug'lar |
| **B — oson** | Haiku | `scout` | Qidiruv, o'qish, xulosa, log tahlili |
| **C — ommaviy** | DeepSeek Flash | `bulk-worker` | Ko'p fayldagi takroriy ish, boilerplate, testlar, tarjima |

**Asosiy qoidalar:**
1. Vazifa 2–3 qadamdan kichik bo'lsa, Opus uni **o'zi bajaradi**.
2. DeepSeek'ga **maxfiy ma'lumot** (`.env`, kalitlar, `memory.db`, foydalanuvchi ma'lumotlari) yuborilmaydi.
3. DeepSeek natijasidan Opus **har doim namuna olib tekshiradi**.
4. Subagent 2 marta xato qilsa, vazifa bir daraja yuqoriga ko'tariladi (C → A → S).

To'liq qoidalar: [`CLAUDE.md`](CLAUDE.md).

## 📁 Tuzilma

```
.
├── CLAUDE.md                  # Dirijyor ko'rsatmalari + loyiha xaritasi
├── .claude/
│   ├── settings.json          # Asosiy model: opus; .env/memory.db o'qish taqiqlangan
│   └── agents/
│       ├── scout.md           # Haiku — qidiruv / o'qish (faqat o'qish)
│       ├── builder.md         # Sonnet — o'rta ishlar
│       └── bulk-worker.md     # Haiku koordinator → DeepSeek MCP
├── server.py, voice.py
├── hermes/                    # orchestrator, config, memory, telegram, documents
├── prompts/
├── deploy/
└── .env.example               # Hermes bot sozlamalari
```

## ⚙️ O'rnatish

### 1. Talablar
- [Claude Code](https://docs.claude.com/en/docs/claude-code) (Max/Pro obuna yoki API kalit)
- Python 3.10–3.12 (DeepSeek MCP server uchun)
- DeepSeek API kalit: https://platform.deepseek.com

### 2. DeepSeek subagentni o'rnatish
[PsChina/deepseek-as-subagent](https://github.com/PsChina/deepseek-as-subagent):
```bash
git clone https://github.com/PsChina/deepseek-as-subagent
cd deepseek-as-subagent
# install.sh va requirements.lock ni ko'rib chiqing, so'ng:
./install.sh
```
`install.sh` MCP serverni Claude Code'ga **o'zi ro'yxatdan o'tkazadi** — shuning uchun bu repoda `.mcp.json` yo'q.

API kalit loyihaning `.env` fayliga emas, `~/.deepseek-mcp/config.json` ga yoziladi (Windows'da `DEEPSEEK_API_KEY` env o'zgaruvchisi):
```json
{
  "api_key": "sk-...",
  "flash": "deepseek-flash",
  "pro": "deepseek-v4-pro"
}
```
> ⚠️ Bu loyiha yangi. O'rnatishdan oldin kodini ko'rib chiqing. DeepSeek coding rejimida Bash'ni sizning kompyuteringizda ishga tushiradi (OS sandbox emas).

### 3. Claude Code'ni ishga tushirish
```bash
cd hermes
claude
```
Ichkarida `/agents` bilan `scout`, `builder`, `bulk-worker` ko'rinishini, `/mcp` bilan DeepSeek server ulanganini tekshiring.
DeepSeek'ni bir sessiyada o'chirish: `DEEPSEEK_MODE=off claude`.

## ✅ Tekshirish

Subagentlar haqiqatda to'g'ri modelda ishlayotganini tekshiring:

```bash
grep -rhoE '"model":"[^"]+"' ~/.claude/projects/*/*/subagents/ 2>/dev/null | sort | uniq -c
```

Kutilgan natija: `haiku`, `sonnet` va `opus` modellari aralash ko'rinadi.

## 💰 Narx haqida

- Opus, Sonnet va Haiku Claude obunangiz limitidan foydalanadi.
- DeepSeek Flash token uchun alohida to'lanadi: https://api-docs.deepseek.com/quick_start/pricing

## 🗺️ Yo'l xaritasi

- [x] Asosiy skelet: Opus + Sonnet + Haiku agentlar
- [ ] DeepSeek MCP integratsiyasi (o'rnatish va sinab ko'rish)
- [ ] Routing statistikasi (qaysi model qancha ishladi)
- [ ] Avtomatik qiyinlik klassifikatori (RouteLLM g'oyasi asosida)
- [ ] Hermes `orchestrator.py` dagi simulyatsiyani haqiqiy LLM chaqiruviga almashtirish

## 📚 Ilhom manbalari

- [musistudio/claude-code-router](https://github.com/musistudio/claude-code-router)
- [PsChina/deepseek-as-subagent](https://github.com/PsChina/deepseek-as-subagent)
- [BeehiveInnovations/pal-mcp-server](https://github.com/BeehiveInnovations/pal-mcp-server)
- [Yeachan-Heo/oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)
- [lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM)
