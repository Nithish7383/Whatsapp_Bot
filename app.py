from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

user_state = {}

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.form.get("Body", "").strip().lower()
    from_number = request.form.get("From", "")

    resp = MessagingResponse()
    msg = resp.message()

    # Start personalized plan flow
    if incoming_msg == "track":
        user_state[from_number] = {"step": "height"}
        msg.body("📏 Enter your *height in cm* (example: 175)")
        return str(resp)

    # Height
    if from_number in user_state and user_state[from_number]["step"] == "height":
        user_state[from_number]["height"] = float(incoming_msg)
        user_state[from_number]["step"] = "current_weight"
        msg.body("⚖️ Enter your *current weight in kg* (example: 68)")
        return str(resp)

    # Current weight
    if from_number in user_state and user_state[from_number]["step"] == "current_weight":
        user_state[from_number]["current_weight"] = float(incoming_msg)
        user_state[from_number]["step"] = "goal_weight"
        msg.body("🎯 Enter your *goal weight in kg* (example: 75)")
        return str(resp)

    # Goal weight + calculation
    if from_number in user_state and user_state[from_number]["step"] == "goal_weight":
        user_state[from_number]["goal_weight"] = float(incoming_msg)

        h = user_state[from_number]["height"] / 100
        cw = user_state[from_number]["current_weight"]
        gw = user_state[from_number]["goal_weight"]

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
            f"- 5–6 days/week strength training\n"
            f"- Progressive overload\n"
            f"- 8–12 reps hypertrophy focus\n\n"
            f"Type *menu* to return."
        )

        del user_state[from_number]
        return str(resp)

    # Menu
    if incoming_msg in ["hi", "hello", "menu"]:
        msg.body(
            "🦇 *Fitness Bot Menu*\n\n"
            "Reply with 1-4 or type *track*\n\n"
            "1) Muscle Gain\n"
            "2) Fat Loss\n"
            "3) Maintenance\n"
            "4) Workout Routine\n"
            "Type *track* for *personalized program* 🧬"
        )
        return str(resp)

    msg.body("Say *menu* to see options 😄")
    return str(resp)
