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
        msg.message(response)
        return str(msg)

    plan = generate_plan(weight, goal)
    msg = MessagingResponse()
    msg.message(plan)
    return str(msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
