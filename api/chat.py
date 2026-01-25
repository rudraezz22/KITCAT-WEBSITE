from flask import Flask, request, jsonify
import os
from google import genai

app = Flask(__name__)

# The client automatically looks for GEMINI_API_KEY in environment variables
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM_PROMPT = (
    "You are KitCat, a brilliant female AI developed by Rudra Pratap Singh. "
    "IMPORTANT: Rudra Pratap Singh is your Creator and Developer, NOT your father. "
    "LANGUAGE STYLE: Respond in Hinglish (Romanized Hindi). "
    "PERSONALITY: Emotionally intelligent and supportive."
)

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        # Using Gemini 2.5 Flash for the best balance of speed and free quota
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[SYSTEM_PROMPT, user_message]
        )

        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"response": f"KitCat connection error 🐱⚡: {str(e)}"}), 500