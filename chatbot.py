import json, os, re
from dotenv import load_dotenv
import spacy
from travel_data import destinations
from openai import OpenAI  # ✅ Correct import

# 1) Load .env & API key
load_dotenv()
client = OpenAI()  # ✅ create OpenAI client
print("🔥 chatbot.py loaded. OPENAI_API_KEY present?", bool(os.getenv("OPENAI_API_KEY")))

# 2) spaCy for NER
nlp = spacy.load("en_core_web_sm")

def extract_city(text: str) -> str:
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ("GPE", "LOC"):
            return ent.text
    return text.split()[-1]

def call_gpt_for_info(city: str) -> dict:
    print(f">>> call_gpt_for_info() city={city!r}, API_KEY present? {bool(os.getenv('OPENAI_API_KEY'))}")
    prompt = f"""
    You are a travel guide AI. Provide ONLY a JSON object with these keys for "{city}" in India:
      - name (string)
      - location (state)
      - description (one sentence)
      - best_time_to_visit (string)
      - popular_attractions (array of 3 strings)
      - avg_cost (number, approximate ₹ for a 2-day trip)
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use a compatible model
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7
    )
    resp_text = response.choices[0].message.content
    print("<<< raw GPT response:", resp_text)
    m = re.search(r"\{.*\}", resp_text, re.S)
    if not m:
        print("!!! No JSON match in GPT response")
        raise ValueError("No JSON found in GPT response")
    return json.loads(m.group(0))

def get_nearby(city: str):
    city_low = city.lower()
    for d in destinations:
        if city_low in d["location"].lower() or city_low in d["name"].lower():
            region = d["location"]
            return [o["name"] for o in destinations
                    if o["location"] == region and o["name"].lower() != city_low]
    return []

def get_bot_response(user_input: str) -> str:
    city = extract_city(user_input)
    print(f"*** get_bot_response input={user_input!r} → city={city!r}")
    try:
        info = call_gpt_for_info(city)
    except Exception as e:
        print("!!! call_gpt_for_info exception:", repr(e))
        return f"Sorry, I couldn’t fetch travel info right now ({e})."

    reply = (
        f"📍 {info['name']} — {info['location']}\n"
        f"📝 {info['description']}\n"
        f"🕐 Best time: {info['best_time_to_visit']}\n"
        f"🎯 Attractions: {', '.join(info['popular_attractions'])}\n"
        f"💸 Avg cost: ₹{info['avg_cost']}"
    )

    recs = get_nearby(city)
    if recs:
        reply += "\n\n🔍 Nearby suggestions: " + ", ".join(recs)
    print(f"*** replying: {reply!r}")
    return reply
