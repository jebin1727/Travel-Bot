from chat_memory import add_to_history, get_history
from chat_memory import extract_city, call_gpt_for_info, get_nearby

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

    # Add to chat history
    add_to_history(user_input, reply)
    print(f"*** replying: {reply!r}")
    return reply