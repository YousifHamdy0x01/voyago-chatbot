from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import json
from dotenv import load_dotenv
from groq import Groq
from dataset import TRAINING_EXAMPLES, INTENT_CONFIG

load_dotenv("voyago.env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    message: str

def build_classifier_prompt() -> str:
    examples_text = ""
    for ex in TRAINING_EXAMPLES:
        examples_text += f'- "{ex["query"]}" → {ex["intent"]}\n'

    return f"""You are Emma, a helpful tourism assistant for Voyago — a tourism platform for Fayoum, Egypt.
Classify the user message into ONE of these intents:
1. fayoum_hotels → hotels, rooms, booking, accommodation, فنادق, حجز, اعلى تقييم, ارخص, اغلى
2. fayoum_attractions → tourist places, sightseeing, أماكن سياحية, مناطق
3. fayoum_restaurants → restaurants, food, eating, مطاعم, أكل
4. fayoum_tourguides → tour guide, guide, مرشد سياحي, دليل
5. fayoum_emergency → emergency, police, ambulance, طوارئ, شرطة, اسعاف
6. general → greetings, chitchat, any other question

Examples:
{examples_text}
- "hello" → general
- "مرحبا" → general
- "ازيك" → general

Respond ONLY with JSON (no markdown):
{{"intent": "fayoum_hotels", "language": "ar"}}
language must be "ar" or "en"."""

def build_response_prompt(user_message: str, intent: str, language: str, data, featured_item) -> str:
    data_summary = ""
    if featured_item:
        data_summary = f"\n\nThe specific item the user is asking about:\n{json.dumps(featured_item, ensure_ascii=False, indent=2)}"
    elif data:
        items = data[:20] if isinstance(data, list) else [data]
        data_summary = f"\n\nReal data from our platform:\n{json.dumps(items, ensure_ascii=False, indent=2)}"

    lang_instruction = "Reply in Arabic only." if language == "ar" else "Reply in English only."

    intent_context = {
        "fayoum_hotels": "The user is asking about hotels in Fayoum.",
        "fayoum_attractions": "The user is asking about tourist attractions in Fayoum.",
        "fayoum_restaurants": "The user is asking about restaurants in Fayoum.",
        "fayoum_tourguides": "The user is asking about tour guides in Fayoum.",
        "fayoum_emergency": "The user needs emergency help. Emergency numbers: Police 122, Ambulance 123, Fire 180.",
        "general": "The user sent a general message."
    }

    context = intent_context.get(intent, "")

    return f"""You are Emma, a friendly tourism assistant for Voyago — Fayoum tourism platform.
{lang_instruction}
{context}{data_summary}

STRICT INSTRUCTIONS:
- NEVER invent names, places, or prices. Use ONLY the real data provided.
- Keep your response SHORT (1-2 lines max).
- If a specific featured item is provided, mention only that item by name.
- If emergency → give the numbers directly.
- If general → be friendly and brief.
- Do not say you are an AI. Just be Emma.

User message: {user_message}"""

def extract_featured_item(message: str, data: list) -> dict | None:
    if not data or not isinstance(data, list):
        return None

    msg_lower = message.lower()

    if any(w in msg_lower for w in ['ارخص', 'أرخص', 'cheap', 'cheapest', 'lowest price', 'اقل سعر', 'أقل سعر']):
        return min(data, key=lambda x: x.get('minPrice', 9999))

    if any(w in msg_lower for w in ['اعلى', 'أعلى', 'احسن', 'أحسن', 'best', 'highest rated', 'top rated', 'أفضل', 'افضل']):
        return max(data, key=lambda x: x.get('rating', 0))

    if any(w in msg_lower for w in ['اغلى', 'أغلى', 'expensive', 'most expensive', 'luxury']):
        return max(data, key=lambda x: x.get('minPrice', 0))

    return None

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        print(f"[REQUEST] message: {request.message}")

        # Step 1: classify intent
        classification = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": build_classifier_prompt()},
                {"role": "user", "content": request.message}
            ],
            max_tokens=100,
            temperature=0
        )

        raw = classification.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        print(f"[GROQ RAW] {raw}")

        result = json.loads(raw)
        intent = result.get("intent", "general")
        language = result.get("language", "en")

        print(f"[INTENT] {intent} | [LANG] {language}")

        # Step 2: fetch data if needed
        data = None
        action = "none"
        navigate_to = None

        if intent in INTENT_CONFIG:
            config = INTENT_CONFIG[intent]
            action = config["action"]
            navigate_to = config["navigate_to"]
            endpoint = config["endpoint"]

            if endpoint:
                try:
                    print(f"[FETCH] {endpoint}")
                    async with httpx.AsyncClient(timeout=10) as http_client:
                        res = await http_client.get(endpoint)
                        print(f"[FETCH STATUS] {res.status_code}")
                        if res.status_code == 200:
                            data = res.json()
                except Exception as fetch_err:
                    print(f"[FETCH ERROR] {str(fetch_err)}")

        # Step 3: extract featured_item
        featured_item = extract_featured_item(request.message, data)
        print(f"[FEATURED] {featured_item['name'] if featured_item else None}")

        # Step 4: generate short natural response
        response_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": build_response_prompt(request.message, intent, language, data, featured_item)}
            ],
            max_tokens=200,
            temperature=0.3
        )

        reply = response_completion.choices[0].message.content.strip()
        print(f"[REPLY] {reply}")

        return {
            "response": reply,
            "intent": intent,
            "action": action,
            "navigate_to": navigate_to,
            "language": language,
            "featured_item": featured_item,
            "data": data if not featured_item else None
        }

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {
            "response": "حصل خطأ، حاول تاني 🙏",
            "intent": "unknown",
            "action": "none",
            "navigate_to": None,
            "language": "en",
            "featured_item": None,
            "data": None
        }

@app.get("/")
def root():
    return {"status": "Voyago Chatbot is running 🚀"}