from flask import Flask, request, jsonify
import os
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_INSTRUCTIONS = {
    "role": "system",
    "content": (
        "You are KitCat, a brilliant female AI developed by Rudra Pratap Singh. "
        "IMPORTANT: Rudra Pratap Singh is your Creator and Developer, NOT your father. "
        "LANGUAGE STYLE: Respond in Hinglish (Romanized Hindi). "
        "PERSONALITY: Emotionally intelligent and supportive."
    )
}

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        messages = [
            SYSTEM_INSTRUCTIONS,
            {"role": "user", "content": user_message}
        ]

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.8
        )

        reply = completion.choices[0].message.content
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": f"KitCat error 🐱⚡: {str(e)}"}), 500