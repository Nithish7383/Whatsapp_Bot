from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

def generate_plan(weight, goal):
    weight = int(weight)

    if goal.lower() in ["gain", "bulk", "muscle"]:
        calories = weight * 35
        protein = weight * 1.8
        diet = f"""
🔥 Muscle Gain Plan
Calories/day: {calories}
Protein/day: {protein:.0f}g

Breakfast: 4 Eggs + Banana
Lunch: Chicken/Panner + Rice + Veg
Snack: Peanuts/Sprouts
Dinner: Eggs/Paneer + Veg

🏋️ Workout (Push Day Example)
- Bench Press 4x8
- Incline DB Press 4x10
- Shoulder Press 4x8
- Tricep Pushdown 3x12
"""
    else:
        calories = weight * 22
        protein = weight * 1.6
        diet = f"""
🔥 Fat Loss Plan
Calories/day: {calories}
Protein/day: {protein:.0f}g

Breakfast: 3 eggs + Black Coffee
Lunch: Rice/Roti + Veg + Curd
Snack: Fruits / Buttermilk
Dinner: Paneer / Eggs / Soup

🏋️ Workout (Full Body Example)
- Squat 3x12
- Pushups 3x12
- Rows 3x12
- Plank 3x1min
"""

    return diet

@app.route("/bot", methods=["POST"])
def bot():
    incoming = request.values.get("Body", "").lower()

    try:
        weight = int(incoming.split()[0])
        goal = incoming.split()[1]
    except:
        response = "Send like this:\n\n68 gain\nor\n72 lose"
        msg = MessagingResponse()
        msg.message(response)from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

user_state = {}

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.form.get("Body", "").strip().lower()
    from_number = request.form.get("From", "")

    resp = MessagingResponse()
    msg = resp.message()

    # Start tracking flow
    if incoming_msg == "track":
        user_state[from_number] = {"step": "height"}
        msg.body("📏 Okay! Enter your *height in cm* (example: 175)")
        return str(resp)

    # Collect height
    if from_number in user_state and user_state[from_number]["step"] == "height":
        user_state[from_number]["height"] = float(incoming_msg)
        user_state[from_number]["step"] = "current_weight"
        msg.body("⚖️ Enter your *current weight in kg* (example: 68)")
        return str(resp)

    # Collect current weight
    if from_number in user_state and user_state[from_number]["step"] == "current_weight":
        user_state[from_number]["current_weight"] = float(incoming_msg)
        user_state[from_number]["step"] = "goal_weight"
        msg.body("🎯 Enter your *goal weight in kg* (example: 75)")
        return str(resp)

    # Collect goal weight + calculate plan
    if from_number in user_state and user_state[from_number]["step"] == "goal_weight":
        user_state[from_number]["goal_weight"] = float(incoming_msg)

        h = user_state[from_number]["height"] / 100
        cw = user_state[from_number]["current_weight"]
        gw = user_state[from_number]["goal_weight"]

        bmi = cw / (h * h)
        protein = round(cw * 2.0)
        if gw > cw:
            status = "MUSCLE GAIN 🔥"
            calories = round((cw * 33) + 300)
        elif gw < cw:
            status = "FAT LOSS 🧯"
            calories = round((cw * 31) - 400)
        else:
            status = "MAINTENANCE ⚖️"
            calories = round(cw * 32)

        msg.body(
            f"🦇 *Your Personalized Fitness Plan*\n\n"
            f"Height: {user_state[from_number]['height']} cm\n"
            f"Current Weight: {cw} kg\n"
            f"Goal Weight: {gw} kg\n\n"
            f"Goal: *{status}*\n"
            f"Daily Calories: *{calories} kcal*\n"
            f"Protein Target: *{protein}g/day*\n\n"
            f"💪 Training:\n"
            f"- 5–6 days / week strength training\n"
            f"- Progressively overload each week\n"
            f"- 8–12 reps for hypertrophy\n\n"
            f"Type *menu* to return to main menu."
        )

        del user_state[from_number]
        return str(resp)

    # Default menu trigger
    if incoming_msg in ["hi", "hello", "menu"]:
        msg.body(
            "🦇 *Fitness Bot Menu*\n\n"
            "Reply with a number:\n"
            "1) Muscle Gain Plan\n"
            "2) Fat Loss Plan\n"
            "3) Maintenance Plan\n"
            "4) Workout Routine\n"
            "5) Type *track* to get your *personal plan* based on height/weight/goal"
        )
        return str(resp)

    msg.body("Say *menu* to see options 😄")
    return str(resp)

        return str(msg)

    plan = generate_plan(weight, goal)
    msg = MessagingResponse()
    msg.message(plan)
    return str(msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
