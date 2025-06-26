from travel_data import destinations
import random

def generate_travel_plan(location):
    for place in destinations:
        if location.lower() in place["name"].lower() or location.lower() in place["location"].lower():
            return {
                "destination": place["name"],
                "description": place["description"],
                "best_time": place["best_time_to_visit"],
                "must_visit": place["popular_attractions"],
                "estimated_cost": place["avg_cost"]
            }
    return {"message": "Sorry, I couldn't find a detailed plan for that place."}
