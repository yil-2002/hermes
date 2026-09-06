import asyncio
from hermes.config import Config
from hermes.memory import MemoryStore

class HermesOrchestrator:
    def __init__(self, db: MemoryStore):
        self.db = db
        
    async def handle(self, message: str, session_id: str, image_urls=None, document_text=None) -> str:
        # 1. Byudjet tekshiruvi (Budget Cap)
        spent = self.db.get_today_spend()
        degrade_to_t1 = False
        
        if Config.DAILY_BUDGET > 0 and spent >= Config.DAILY_BUDGET:
            # Context Overflow Fast-Fail
            total_context_len = len(message) + (len(document_text) if document_text else 0)
            if total_context_len > Config.T1_CONTEXT_TOKENS:
                return "⚠️ Kunlik token byudjeti tugaganligi sababli, katta hujjatlarni tahlil qilish vaqtincha cheklandi."
            degrade_to_t1 = True
            
        # 2. Prompt yig'ish
        full_prompt = message
        if document_text:
            full_prompt += f"\n\n[HUJJAT MATNI]:\n{document_text}"

        # 3. Modelni ishga tushirish (Siz bu yerda haqiqiy LiteLLM/OpenAI chaqiruvni bog'laysiz)
        try:
            # MoE Routing qoidasi
            tier = "Tier-1" if degrade_to_t1 else ("Tier-3 (Vision/Doc)" if document_text or image_urls else "Tier-2 (Deep)")
            
            # --- SHU YERGA LLM (Groq/Llama/Gemini) CHAQIRUVINI QO'SHASIZ ---
            await asyncio.sleep(2) # Simulyatsiya
            answer = f"Yechim tayyorlandi.\n\n`[MoE Router: {tier}]`"
            
            # Xarajatni ledger'ga yozish (simulyatsiya tokenlari)
            self.db.add_spend(tokens_in=250, tokens_out=150)
            return answer
        except Exception as e:
            return f"❌ Model xatosi: {str(e)}"
