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

To'liq qoidalar: [agent/rules/routing.md](https://github.com/yil-2002/agent/blob/main/rules/routing.md).

## ⚙️ O'rnatish

Agentlar (`.claude/agents/`) va routing qoidalari (`.claude/rules/dirijyor-routing.md`)
[`yil-2002/agent`](https://github.com/yil-2002/agent) dan nusxalangan, shuning uchun ular bulut sessiyalarida ham,
kompyuterda ham repo ochilishi bilan ishlaydi. Yangilash:

```bash
/yo'l/agent/scripts/install-to-repo.sh .
```

```
.
├── CLAUDE.md                  # Hermes'ga xos ma'lumot: fayl xaritasi, tekshirish
├── .claude/
│   ├── settings.json          # model: opus; .env/memory.db o'qish taqiqlangan
│   ├── agents/                # scout, builder, bulk-worker (agent repodan nusxa)
│   └── rules/dirijyor-routing.md
├── server.py, voice.py
├── hermes/                    # orchestrator, config, memory, telegram, documents
├── prompts/
├── deploy/
└── .env.example               # Hermes bot sozlamalari
```

DeepSeek o'rnatish — plugin README'sida.

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
- [x] Umumiy qismni `dirijyor` plugin'iga ajratish
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
