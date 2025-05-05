import json
import hashlib
from sklearn.metrics.pairwise import cosine_similarity
import os

# ========================
# 1. DATA INITIALIZATION
# ========================

DESTINATIONS = {
    # ================= BEACH DESTINATIONS =================
    # Asia (Beach)
    "d1": {  # Low budget
        "name": "Phuket Backpackers Hostel",
        "type": "beach",
        "region": "asia",
        "location": "Phuket, Thailand",
        "price": 80,
        "tags": {"beach": 0.9, "backpacking": 0.8},
        "ideal_weather": ["sunny", "warm"],
        "activities": ["Snorkeling", "Spa"],  # Only from beach activities
        "accommodation": ["Hotel"],  # Only from your list
        "cuisines": ["Local", "Street food"]  # Only from your list
    },
    "d2": {  # Medium budget
        "name": "Bali Beach Resort",
        "type": "beach",
        "region": "asia",
        "location": "Bali, Indonesia",
        "price": 350,
        "tags": {"beach": 0.9, "luxury": 0.7},
        "ideal_weather": ["sunny", "warm"],
        "activities": ["Surfing", "Spa"],
        "accommodation": ["Hotel", "Villa"],
        "cuisines": ["Seafood", "Local"]
    },
    "d3": {  # High budget
        "name": "Maldives Overwater Villa",
        "type": "beach",
        "region": "asia",
        "location": "Maldives",
        "price": 800,
        "tags": {"beach": 0.95, "luxury": 0.9},
        "ideal_weather": ["sunny", "warm"],
        "activities": ["Surfing", "Spa"],
        "accommodation": ["Villa"],
        "cuisines": ["Seafood", "Vegetarian"]
    },

    # Europe (Beach)
    "d4": {  # Low budget
        "name": "Algarve Surf Hostel",
        "type": "beach",
        "region": "europe",
        "location": "Portugal",
        "price": 70,
        "tags": {"beach": 0.8, "surfing": 0.9},
        "ideal_weather": ["sunny", "warm"],
        "activities": ["Surfing"],
        "accommodation": ["Hotel"],
        "cuisines": ["Seafood", "Local"]
    },
    "d5": {  # Medium budget
        "name": "Santorini Cliff Hotel",
        "type": "beach",
        "region": "europe",
        "location": "Greece",
        "price": 350,
        "tags": {"beach": 0.85, "romantic": 0.9},
        "ideal_weather": ["sunny", "warm"],
        "activities": ["Spa"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Vegetarian"]
    },
    "d6": {  # High budget
        "name": "French Riviera Villa",
        "type": "beach",
        "region": "europe",
        "location": "France",
        "price": 900,
        "tags": {"beach": 0.9, "luxury": 0.95},
        "ideal_weather": ["sunny", "warm"],
        "activities": ["Spa"],
        "accommodation": ["Villa"],
        "cuisines": ["Local", "Gourmet"]
    },

    # Africa (Beach)
    "d7": {  # Low budget
        "name": "Zanzibar Guesthouse",
        "type": "beach",
        "region": "africa",
        "location": "Tanzania",
        "price": 60,
        "tags": {"beach": 0.85, "cultural": 0.7},
        "ideal_weather": ["sunny", "warm"],
        "activities": ["Snorkeling"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Seafood"]
    },
    "d8": {  # Medium budget
        "name": "Diani Beach Resort",
        "type": "beach",
        "region": "africa",
        "location": "Kenya",
        "price": 350,
        "tags": {"beach": 0.9, "wildlife": 0.6},
        "ideal_weather": ["sunny", "warm"],
        "activities": ["Snorkeling", "Spa"],
        "accommodation": ["Hotel"],
        "cuisines": ["Seafood", "Local"]
    },
    "d9": {  # High budget
        "name": "Seychelles Private Island",
        "type": "beach",
        "region": "africa",
        "location": "Seychelles",
        "price": 1200,
        "tags": {"beach": 0.95, "exclusive": 0.9},
        "ideal_weather": ["sunny", "warm"],
        "activities": ["Spa"],
        "accommodation": ["Villa"],
        "cuisines": ["Seafood", "Vegetarian"]
    },

    # ================= MOUNTAIN DESTINATIONS =================
    # Asia (Mountain)
    "d10": {  # Low budget
        "name": "Pokhara Trekking Lodge",
        "type": "mountain",
        "region": "asia",
        "location": "Nepal",
        "price": 40,
        "tags": {"mountain": 0.9, "trekking": 0.8},
        "ideal_weather": ["cool", "dry"],
        "activities": ["Mountain climbing"],
        "accommodation": ["Hotel"],
        "cuisines": ["Vegetarian", "Local"]
    },
    "d11": {  # Medium budget
        "name": "Himalayan Eco Resort",
        "type": "mountain",
        "region": "asia",
        "location": "Bhutan",
        "price": 320,
        "tags": {"mountain": 0.9, "spiritual": 0.7},
        "ideal_weather": ["cool", "dry"],
        "activities": ["Mountain climbing"],
        "accommodation": ["Hotel"],
        "cuisines": ["Vegetarian", "Local"]
    },
    "d12": {  # High budget
        "name": "Japanese Alps Ryokan",
        "type": "mountain",
        "region": "asia",
        "location": "Japan",
        "price": 500,
        "tags": {"mountain": 0.9, "luxury": 0.8},
        "ideal_weather": ["snowy", "cold"],
        "activities": ["Skiing"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Vegetarian"]
    },

    # Europe (Mountain)
    "d13": {  # Low budget
        "name": "Slovakian Mountain Hut",
        "type": "mountain",
        "region": "europe",
        "location": "Slovakia",
        "price": 50,
        "tags": {"mountain": 0.8, "hiking": 0.9},
        "ideal_weather": ["cool", "sunny"],
        "activities": ["Mountain climbing"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Meat"]
    },
    "d14": {  # Medium budget
        "name": "Austrian Alpine Hotel",
        "type": "mountain",
        "region": "europe",
        "location": "Austria",
        "price": 400,
        "tags": {"mountain": 0.9, "skiing": 0.8},
        "ideal_weather": ["snowy", "cold"],
        "activities": ["Skiing"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Meat"]
    },
    "d15": {  # High budget
        "name": "Swiss Luxury Chalet",
        "type": "mountain",
        "region": "europe",
        "location": "Switzerland",
        "price": 1000,
        "tags": {"mountain": 0.95, "luxury": 0.9},
        "ideal_weather": ["snowy", "cold"],
        "activities": ["Skiing"],
        "accommodation": ["Villa"],
        "cuisines": ["Local", "Vegetarian"]
    },

    # Africa (Mountain)
    "d16": {  # Low budget
        "name": "Atlas Mountain Camp",
        "type": "mountain",
        "region": "africa",
        "location": "Morocco",
        "price": 60,
        "tags": {"mountain": 0.8, "cultural": 0.7},
        "ideal_weather": ["cool", "dry"],
        "activities": ["Mountain climbing"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Vegetarian"]
    },
    "d17": {  # Medium budget
        "name": "Mount Kenya Lodge",
        "type": "mountain",
        "region": "africa",
        "location": "Kenya",
        "price": 450,
        "tags": {"mountain": 0.85, "wildlife": 0.6},
        "ideal_weather": ["cool", "dry"],
        "activities": ["Mountain climbing"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Meat"]
    },
    "d18": {  # High budget
        "name": "Kilimanjaro Luxury Camp",
        "type": "mountain",
        "region": "africa",
        "location": "Tanzania",
        "price": 700,
        "tags": {"mountain": 0.9, "luxury": 0.8},
        "ideal_weather": ["cool", "dry"],
        "activities": ["Mountain climbing"],
        "accommodation": ["Villa"],
        "cuisines": ["Local", "Vegetarian"]
    },

    # ================= CITY DESTINATIONS =================
    # Asia (City)
    "d19": {  # Low budget
        "name": "Hanoi Backpackers",
        "type": "city",
        "region": "asia",
        "location": "Vietnam",
        "price": 175,
        "tags": {"city": 0.8, "cultural": 0.9},
        "ideal_weather": ["warm", "humid"],
        "activities": ["Shopping", "Museums"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Street food"]
    },
    "d20": {  # Medium budget
        "name": "Bangkok City Hotel",
        "type": "city",
        "region": "asia",
        "location": "Thailand",
        "price": 420,
        "tags": {"city": 0.85, "shopping": 0.8},
        "ideal_weather": ["warm", "humid"],
        "activities": ["Shopping", "City tours"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Street food"]
    },
    "d21": {  # High budget
        "name": "Tokyo Luxury Tower",
        "type": "city",
        "region": "asia",
        "location": "Japan",
        "price": 850,
        "tags": {"city": 0.95, "luxury": 0.9},
        "ideal_weather": ["mild", "seasonal"],
        "activities": ["Shopping", "Museums"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Vegetarian"]
    },

    # Europe (City)
    "d22": {  # Low budget
        "name": "Krakow Hostel",
        "type": "city",
        "region": "europe",
        "location": "Poland",
        "price": 100,
        "tags": {"city": 0.8, "historical": 0.9},
        "ideal_weather": ["mild", "seasonal"],
        "activities": ["Museums", "City tours"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Meat"]
    },
    "d23": {  # Medium budget
        "name": "Barcelona City Flat",
        "type": "city",
        "region": "europe",
        "location": "Spain",
        "price": 470,
        "tags": {"city": 0.9, "cultural": 0.8},
        "ideal_weather": ["warm", "sunny"],
        "activities": ["Museums", "City tours"],
        "accommodation": ["Apartment"],
        "cuisines": ["Local", "Seafood"]
    },
    "d24": {  # High budget
        "name": "Paris Luxury Suite",
        "type": "city",
        "region": "europe",
        "location": "France",
        "price": 850,
        "tags": {"city": 0.95, "luxury": 0.9},
        "ideal_weather": ["mild", "seasonal"],
        "activities": ["Museums", "Shopping"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Vegetarian"]
    },

    # Africa (City)
    "d25": {  # Low budget
        "name": "Marrakech Hostel",
        "type": "city",
        "region": "africa",
        "location": "Morocco",
        "price": 40,
        "tags": {"city": 0.8, "cultural": 0.9},
        "ideal_weather": ["warm", "dry"],
        "activities": ["Shopping", "Museums"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Street food"]
    },
    "d26": {  # Medium budget
        "name": "Cape Town Boutique Hotel",
        "type": "city",
        "region": "africa",
        "location": "South Africa",
        "price": 180,
        "tags": {"city": 0.85, "scenic": 0.8},
        "ideal_weather": ["warm", "sunny"],
        "activities": ["Shopping", "City tours"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Seafood"]
    },
    "d27": {  # High budget
        "name": "Dubai Skyscraper Hotel",
        "type": "city",
        "region": "asia",
        "location": "UAE",
        "price": 900,
        "tags": {"city": 0.95, "luxury": 0.9},
        "ideal_weather": ["warm", "dry"],
        "activities": ["Shopping", "Museums"],
        "accommodation": ["Hotel"],
        "cuisines": ["Local", "Vegetarian"]
    }
}


def load_users():
    if os.path.exists('users.json'):
        try:
            with open('users.json', 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: Corrupted user file. Starting fresh.")
    return {}


USERS = load_users()


class TravelCompanion:
    def __init__(self):
        self.current_user = None
        self.last_recommendations = []

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self):
        print("\n" + "=" * 20)
        print(" NEW USER REGISTRATION")
        print("=" * 20 + "\n")

        while True:
            username = input("Choose a username: ").strip()
            if not username:
                print("Username cannot be empty!")
                continue
            if username in USERS:
                print("Username already exists!")
                continue
            break

        password = input("Choose a password: ").strip()

        USERS[username] = {
            "password": self.hash_password(password),
            "preferences": None,
            "ratings": {}
        }
        self.save_users()
        self.current_user = username
        print(f"\nWelcome, {username}! Let's set your travel preferences.")
        self.set_preferences()
        return True

    def login(self):
        print("\n" + "=" * 20)
        print(" USER LOGIN")
        print("=" * 20 + "\n")

        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username in USERS:
            if USERS[username]["password"] == self.hash_password(password):
                self.current_user = username
                print(f"\nWelcome back, {username}!")
                if not USERS[username]["preferences"]:
                    print("Please complete your travel preferences first.")
                    self.set_preferences()
                return True

        print("\nInvalid credentials or user doesn't exist.")
        return False

    def set_preferences(self):
        print("\n" + "=" * 20)
        print(" TRAVEL PREFERENCES")
        print("=" * 20 + "\n")

        print("We'll ask a few questions to personalize your experience:\n")

        trip_type = self._ask_multichoice("What type of trip do you prefer?",
                                          ["Beach", "Mountain", "City"])

        preferences = {
            "trip_type": trip_type,
            "budget": self._ask_multichoice("What's your budget range?",
                                            ["Low ($0-$300)", "Medium ($300-$500)", "High ($500+)"],
                                            prices=[(0, 300), (300, 500), (500, 9999)]),
            "activities": self._ask_activities(trip_type.lower()),
            "accommodation": self._ask_multichoice(
                "Preferred accommodation type:",
                ["Hotel", "Villa", "Apartment"]
            ),
            "cuisine": self._ask_cuisines(),
            "travel_season": None  # Will be set below
        }

        # Ask about travel season as part of preferences
        print("\n" + "=" * 20)
        print(" TRAVEL PLANNING")
        print("=" * 20 + "\n")
        preferences["travel_season"] = self._ask_multichoice(
            "When are you planning to travel?",
            ["Summer", "Winter", "Spring", "Fall"]
        ).lower()

        USERS[self.current_user]["preferences"] = preferences
        self.save_users()
        print("\nPreferences saved successfully!")

    def _ask_multichoice(self, question, options, prices=None):
        print(f"\n{question}")
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")

        while True:
            try:
                choice = int(input("Your choice (1-{}): ".format(len(options))))
                if 1 <= choice <= len(options):
                    if prices:
                        return {"choice": options[choice - 1].lower(),
                                "price_range": prices[choice - 1]}
                    return options[choice - 1].lower()
                print("Invalid choice number.")
            except ValueError:
                print("Please enter a number.")

    def _ask_activities(self, trip_type):
        activity_groups = {
            "beach": ["Surfing", "Snorkeling", "Spa"],
            "mountain": ["Skiing", "Snowboarding", "Mountain climbing"],
            "city": ["Shopping", "Museums", "City tours"]
        }

        print("\nSelect activities (enter numbers separated by spaces):")
        activities = activity_groups[trip_type]

        for i, activity in enumerate(activities, 1):
            print(f"{i}. {activity}")

        while True:
            selections = input(">> ").strip().split()
            try:
                selected_activities = [activities[int(s) - 1].lower() for s in selections if
                                       s.isdigit() and 0 < int(s) <= len(activities)]
                if selected_activities:
                    return selected_activities
                print("Please select at least one valid activity.")
            except (ValueError, IndexError):
                print("Invalid selection. Try again.")

    def _ask_cuisines(self):
        cuisines = [
            "Local", "Vegetarian", "Seafood",
            "Street food", "Meat", "Vegan"
        ]

        print("\nSelect cuisines (enter numbers separated by spaces):")
        for i, cuisine in enumerate(cuisines, 1):
            print(f"{i}. {cuisine}")

        while True:
            selections = input(">> ").strip().split()
            try:
                selected_cuisines = [cuisines[int(s) - 1].lower() for s in selections if
                                     s.isdigit() and 0 < int(s) <= len(cuisines)]
                if selected_cuisines:
                    return selected_cuisines
                print("Please select at least one valid cuisine.")
            except (ValueError, IndexError):
                print("Invalid selection. Try again.")

    def get_recommendations(self):
        print("\n" + "=" * 20)
        print(" TRAVEL RECOMMENDATIONS")
        print("=" * 20 + "\n")

        if not self.current_user or not USERS[self.current_user]["preferences"]:
            print("Please set your preferences first!")
            return

        user_prefs = USERS[self.current_user]["preferences"]

        # Get the stored travel season
        season = user_prefs.get("travel_season", "summer")  # default to summer if not set

        weather_map = {
            "summer": "sunny",
            "winter": "snowy",
            "spring": "mild",
            "fall": "rainy"
        }
        weather = weather_map.get(season.lower(), "mild")

        print(f"\nSearching for {weather} weather options (for {season.capitalize()} travel)...\n")

        recommendations = []
        budget_min, budget_max = user_prefs["budget"]["price_range"]

        for dest_id, dest in DESTINATIONS.items():
            # Initial filtering
            if not (budget_min <= dest["price"] <= budget_max):
                continue
            if dest["type"] != user_prefs["trip_type"]:
                continue

            # ACTIVITY MATCHING
            user_activities = set(act.lower() for act in user_prefs["activities"])
            dest_activities = set(act.lower() for act in dest["activities"])
            matched_activities = list(user_activities & dest_activities)

            if not matched_activities and dest["activities"]:
                matched_activities = [dest["activities"][0].lower()]
            if not matched_activities:
                continue

            # Other preference matching
            common_cuisines = set(user_prefs["cuisine"]) & set([c.lower() for c in dest["cuisines"]])
            matching_accom = user_prefs["accommodation"] in dest["accommodation"]

            # Must match at least one preference category
            if not (matched_activities or common_cuisines or matching_accom):
                continue

            # Scoring
            activity_score = len(matched_activities) / max(1, len(user_prefs["activities"]))
            cuisine_score = len(common_cuisines) / max(1, len(user_prefs["cuisine"]))
            accom_score = 1.0 if matching_accom else 0.5
            weather_boost = 1.5 if weather in dest["ideal_weather"] else 0.8

            # Rating score
            rating_score = 1.0
            if dest_id in USERS[self.current_user]["ratings"]:
                rating_score = USERS[self.current_user]["ratings"][dest_id] / 5.0
            elif any(dest_id in user["ratings"] for user in USERS.values()):
                total_ratings = sum(user["ratings"].get(dest_id, 0) for user in USERS.values())
                rating_count = sum(1 for user in USERS.values() if dest_id in user["ratings"])
                rating_score = (total_ratings / rating_count) / 5.0

            # Final score
            total_score = (
                    0.25 * activity_score +
                    0.25 * cuisine_score +
                    0.2 * weather_boost +
                    0.15 * accom_score +
                    0.15 * rating_score
            )

            recommendations.append({
                "id": dest_id,
                "name": dest["name"],
                "location": dest["location"],
                "score": min(100, round(total_score * 100)),
                "price": dest["price"],
                "weather": "Ideal" if weather in dest["ideal_weather"] else "Good",
                "matched_activities": matched_activities,
                "matched_cuisines": list(common_cuisines),
                "accommodation": dest["accommodation"]
            })

        if not recommendations:
            print("\nNo destinations match your criteria. Try adjusting preferences.")
            return

        recommendations.sort(key=lambda x: x["score"], reverse=True)
        self.last_recommendations = recommendations[:3]

        print("\n" + "=" * 20)
        print(" TOP RECOMMENDATIONS")
        print("=" * 20 + "\n")

        for i, rec in enumerate(self.last_recommendations, 1):
            ratings = [user["ratings"].get(rec["id"], 0) for user in USERS.values()
                       if rec["id"] in user["ratings"]]

            print(f"{i}. {rec['name']} ({rec['location']})")
            print(f"   Match Score: {rec['score']}%")
            print(f"   Price: ${rec['price']}")
            if ratings:
                avg_rating = sum(ratings) / len(ratings)
                print(f"   Rating: {avg_rating:.1f}/5")
            print(f"   Weather: {rec['weather']} for {season.capitalize()}")
            print(f"   Activities: {', '.join(rec['matched_activities'])}")
            print(f"   Cuisines: {', '.join(rec['matched_cuisines']) if rec['matched_cuisines'] else '-'}")
            print(f"   Accommodation: {', '.join(rec['accommodation'])}")
            print()

    def rate_destination(self):
        print("\n" + "=" * 20)
        print(" RATE A DESTINATION")
        print("=" * 20 + "\n")

        if not self.current_user:
            print("Please login first!")
            return

        if not self.last_recommendations:
            print("No recent recommendations to rate. Please get recommendations first.")
            return

        print("Available destinations to rate:")
        for rec in self.last_recommendations:
            print(f"{rec['id']}: {rec['name']} ({rec['location']})")

        while True:
            dest_id = input("\nEnter destination ID to rate: ").strip()
            if any(rec['id'] == dest_id for rec in self.last_recommendations):
                break
            print("Invalid destination ID! Please choose from your recent recommendations.")

        while True:
            rating = input("Your rating (1-5 stars): ").strip()
            if rating.isdigit() and 1 <= int(rating) <= 5:
                USERS[self.current_user]["ratings"][dest_id] = int(rating)
                self.save_users()
                print("Rating saved successfully!")
                return
            print("Please enter a number between 1-5")

    def save_users(self):
        with open('users.json', 'w') as f:
            json.dump(USERS, f, indent=2)


def main():
    app = TravelCompanion()

    while True:
        print("\n" + "=" * 20)
        print(" SMART TRAVEL COMPANION")
        print("=" * 20)
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("\nChoose an option (1-3): ").strip()

        if choice == "1":
            if app.login():
                break
        elif choice == "2":
            if app.register_user():
                break
        elif choice == "3":
            print("\nThank you for using Smart Travel Companion!")
            return
        else:
            print("\nInvalid choice. Please try again.")

    while True:
        print("\n" + "=" * 20)
        print(" MAIN MENU")
        print("=" * 20)
        print("1. Get Recommendations")
        print("2. Update Preferences")
        print("3. Rate a Destination")
        print("4. Logout")

        choice = input("\nChoose an option (1-4): ").strip()

        if choice == "1":
            app.get_recommendations()
        elif choice == "2":
            app.set_preferences()
        elif choice == "3":
            app.rate_destination()
        elif choice == "4":
            print("\nLogged out successfully. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()